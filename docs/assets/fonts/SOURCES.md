# Website fonts

| File | Source | Coverage |
| --- | --- | --- |
| `inter-latin-variable.woff2` | Unmodified `package/files/inter-latin-standard-normal.woff2` from [Fontsource Inter 5.3.0](https://registry.npmjs.org/@fontsource-variable/inter/-/inter-5.3.0.tgz) | Latin upright, weight 100–900, optical size 14–32 |
| `noto-sans-sc-ui.woff2` | Subset of [Google Fonts Noto Sans SC](https://github.com/google/fonts/tree/a85815a42757630ce188fdad368c2dfc444d4773/ofl/notosanssc) | Han characters from the website HTML, JS and market JSON files, plus CJK punctuation |
| `noto-sans-sc-common.woff2` | Subset of the same Google Fonts binary | Remaining GB 2312 level-one Chinese characters, used as a fallback for new copy |

The two Chinese subsets retain the original font metadata and weight axis (100–900). Their combined character maps cover all 3,755 GB 2312 level-one Hanzi. Use the UI font before the common fallback and restrict the latter to `U+4E00-9FFF` so existing UI text needs only the first Chinese file.

Both families use the SIL Open Font License 1.1. [Inter-OFL.txt](Inter-OFL.txt) comes from the Fontsource package. [Noto-Sans-SC-OFL.txt](Noto-Sans-SC-OFL.txt) comes from the pinned Google Fonts source. The Inter WOFF2 SHA-256 is `2c295d99e26dcf357d4d01bcf270fd6924b600c9a13dd8c363ef114f4c6976fa`.

## Refreshing the Chinese subsets

After changing UI text or market entries, download the pinned [NotoSansSC variable TTF](https://raw.githubusercontent.com/google/fonts/a85815a42757630ce188fdad368c2dfc444d4773/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf) and run the following in a Python environment from the repository root.

```sh
python -m pip install fonttools==4.68.0 brotli==1.2.1
python tools/build_site_fonts.py "/path/to/NotoSansSC[wght].ttf"
```

The script verifies the source SHA-256, gathers the current site's Han characters, and writes both WOFF2 files into `docs/assets/fonts/`.
