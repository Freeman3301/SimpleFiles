# FontMaster — ALT Linux packaging

RPM/gear packaging for [FontMaster](https://github.com/NICourced/fontmaster),
a library and tool for inspecting, rendering and editing compiled OpenType
fonts.

## Contents

- `fontmaster.spec` — RPM spec. Sources are fetched from the upstream git tag
  (`0.0.2`, no `v` prefix) and renamed to `fontmaster-%version.tar.gz`.
- `.github/workflows/build-rpm.yml` — builds RPM and SRPM inside an ALT
  container on every push and uploads the results as artifacts.

## Packages

| Package | Contents |
|---|---|
| `fontmaster` | shared library `libfontmaster.so.0` |
| `fontmaster-cli` | `fontmaster_cli` command line tool |
| `fontmaster-qt` | `fontmaster_qt` GUI, `.desktop` file and icon |
| `fontmaster-devel` | headers and CMake package files |

## Building

The build needs ALT Linux tooling (`rpmbuild`, `gear`), which is not available
in Termux. Use one of:

### GitHub Actions

Push to the repository (or run the workflow manually) — CI builds in
`registry.altlinux.org/alt/alt:sisyphus` and uploads `*.rpm` / `*.src.rpm`.

### Local, on ALT Linux

```sh
rpmdev-setuptree
ver=$(rpmspec -q --qf '%{version}' fontmaster.spec | head -1)
curl -fL -o ~/rpmbuild/SOURCES/fontmaster-$ver.tar.gz \
  https://github.com/NICourced/fontmaster/archive/refs/tags/$ver.tar.gz
rpmbuild -ba fontmaster.spec
```

Or with gear, once `.gear/rules` are added to a source-containing repo:

```sh
gear -b
```

## Notes

- Upstream requires HarfBuzz >= 15.1. `p11` ships 12.1.0, so the package can
  only be built against **Sisyphus** (harfbuzz 15.1.0). `p10` is older still.
- libjpeg-turbo in ALT is packaged as `libjpeg` / `libjpeg-devel` (it offers
  the turbo API and `libturbojpeg.pc`); there is no `libjpeg-turbo-devel`.
- The Qt GUI uses Qt 5 (`qt5-base-devel`), not Qt 6.
- Upstream CMake does not install the `.desktop` file or icon; the spec
  installs them explicitly.
