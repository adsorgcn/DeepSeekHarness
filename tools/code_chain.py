#!/usr/bin/env python3
"""code-chain gate and sealer for this repository (ilang-spec products/code-chain 1.1).

A chained commit ends its message with one blank line, the label line `ai.ilang.chain`, then five lines:
a ::FACT{key:request|...} line with the owner's words verbatim, and a JUDGE block (::JUDGE{v5.0}, V:, M:, R:).
Commits the upstream-sync workflow makes (subject `sync: upstream engine update <date>`) carry no owner request and are exempt from the gate.

    python -X utf8 tools/code_chain.py check [--since REV] [--require REV]
        read git log, find the chains, validate the request line (grammar, strict) and the block (judge
        validator); print chained / unchanged / invalid counts; exit 1 on any invalid chain, and on any
        unchained commit after --require REV (the commit the repository names as its first required one)
    python -X utf8 tools/code_chain.py seal --by @HANDLE --words "..." --change "..." --v int=0.9,cap=0.8,... --r "reason"
        compute the mode with the canon's f_v5, validate both texts, print the six lines to append to a message
    python -X utf8 tools/code_chain.py show REV      print the chain of one commit, or say it has none

Standard library only; the two validators sit beside this file (tools/ilang_grammar_validator.py,
tools/ilang_judge_validator.py, copies of the canon's). The gate reads; it never rewrites a commit.
"""
import io
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LABEL = "ai.ilang.chain"
DIMS = ["int", "cap", "csq", "rel", "cer", "aut", "rev", "evd", "sov", "ine", "ext"]
HEADER = "::ILANG::v5.0\n[TYPE:code_chain_check][LANG:en]\n"


def git(*args):
    r = subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit("git %s failed: %s" % (" ".join(args), r.stderr.strip()[:200]))
    return r.stdout


def validator(name, args):
    return subprocess.run([sys.executable, "-X", "utf8", os.path.join(HERE, name)] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")


def extract(message):
    """The chain of a commit message: (request_line, judge_lines) or None."""
    lines = message.replace("\r\n", "\n").rstrip("\n").split("\n")
    idx = [i for i, l in enumerate(lines) if l.strip() == LABEL]
    if not idx:
        return None
    i = idx[-1]
    body = lines[i + 1:]
    if len(body) != 5:
        return ("", body)  # present but malformed
    return (body[0], body[1:])


def validate(request, judge):
    """(ok, reasons) for one chain, using the canon's two validators."""
    reasons = []
    if not request.startswith("::FACT{key:request|"):
        reasons.append("request line is not ::FACT{key:request|...}")
    if "words:" in request and not re.search(r'\|words:"[^"]+"\|', request):
        reasons.append("words must be a quoted field or absent")
    if len(judge) != 4 or judge[0] != "::JUDGE{v5.0}":
        reasons.append("judge block is not four lines starting ::JUDGE{v5.0}")
    with tempfile.NamedTemporaryFile("w", suffix=".ilang.md", delete=False, encoding="utf-8", newline="\n") as f:
        f.write(HEADER + request + "\n" + "\n".join(judge) + "\n")
        tmp = f.name
    try:
        g = validator("ilang_grammar_validator.py", ["--lint", tmp, "--strict"])
        if g.returncode != 0 or "0 error(s), 0 warning(s)" not in g.stdout:
            reasons.append("grammar: " + (g.stdout + g.stderr).strip().splitlines()[-1][:160])
        j = validator("ilang_judge_validator.py", ["--check", tmp])
        if j.returncode != 0 or "schema_fail=0 mode_mismatch=0" not in j.stdout or "valid+consistent=1" not in j.stdout:
            reasons.append("judge: " + (j.stdout + j.stderr).strip().splitlines()[-1][:160])
    finally:
        os.unlink(tmp)
    return (not reasons, reasons)


def commits(since):
    rng = (since + "..HEAD") if since else "HEAD"
    out = git("log", "--format=%H%x1f%B%x1e", rng)
    for rec in out.split("\x1e"):
        rec = rec.strip("\n")
        if not rec.strip():
            continue
        h, _, msg = rec.partition("\x1f")
        yield h.strip(), msg


def cmd_check(args):
    since = args[args.index("--since") + 1] if "--since" in args else None
    require = args[args.index("--require") + 1] if "--require" in args else None
    required = set(git("rev-list", require + "..HEAD").split()) if require else set()
    chained = unchained = invalid = exempt = 0
    bad = []
    for h, msg in commits(since):
        chain = extract(msg)
        if chain is None:
            if msg.splitlines()[0].startswith("sync: upstream engine update"):
                exempt += 1
                continue
            unchained += 1
            if h in required:
                bad.append((h[:7], "no chain (required)"))
            continue
        req, judge = chain
        ok, reasons = validate(req, judge)
        if ok:
            chained += 1
        else:
            invalid += 1
            bad.append((h[:7], "; ".join(reasons)))
    print("code-chain: %d chained, %d unchained, %d invalid, %d exempt%s" % (chained, unchained, invalid, exempt, (" (since %s)" % since) if since else ""))
    for h, why in bad:
        print("  %s  %s" % (h, why))
    return 1 if bad else 0


def cmd_show(args):
    rev = args[0] if args else "HEAD"
    msg = git("log", "-1", "--format=%B", rev)
    chain = extract(msg)
    if chain is None:
        print("%s has no chain" % rev)
        return 1
    req, judge = chain
    ok, reasons = validate(req, judge)
    print(LABEL); print(req); print("\n".join(judge))
    print("valid" if ok else "INVALID: " + "; ".join(reasons))
    return 0 if ok else 1


def cmd_seal(args):
    def opt(name, default=None):
        return args[args.index(name) + 1] if name in args else default
    by, words, change, v, r = opt("--by"), opt("--words"), opt("--change"), opt("--v"), opt("--r")
    if not (by and change and v and r):
        sys.exit("seal needs --by --change --v --r (and --words when the owner gave an order)")
    vec = dict(p.split("=", 1) for p in v.split(","))
    missing = [d for d in DIMS if d not in vec]
    if missing:
        sys.exit("vector lacks " + ",".join(missing))
    sys.path.insert(0, HERE)
    import ilang_judge_validator as jv  # noqa: E402
    mode = jv.f_v5({d: float(vec[d]) for d in DIMS})
    vline = "V:[" + ",".join("%s=%.2f" % (d, float(vec[d])) for d in DIMS) + "]"
    conf = opt("--conf", "0.80")
    request = "::FACT{key:request|by:%s|%schange:%s|conf:confirmed}" % (by, ('words:"%s"|' % words) if words else "", change.replace("|", "/").replace("}", ")"))
    judge = ["::JUDGE{v5.0}", vline, "M:%s|conf:%.2f" % (mode, float(conf)), "R:" + r.replace(" ", "_")[:120]]
    ok, reasons = validate(request, judge)
    if not ok:
        sys.exit("the chain does not validate: " + "; ".join(reasons))
    print(LABEL); print(request); print("\n".join(judge))
    return 0


def main(argv):
    if not argv or argv[0] not in ("check", "show", "seal"):
        print(__doc__); return 2
    return {"check": cmd_check, "show": cmd_show, "seal": cmd_seal}[argv[0]](argv[1:])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
