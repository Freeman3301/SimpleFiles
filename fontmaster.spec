%define _unpackaged_files_terminate_build 1

Name: fontmaster
Version: 0.0.2
Release: alt1

Summary: Inspect, render and edit compiled OpenType fonts
License: GPL-3.0-or-later
Group: Graphics
Url: https://github.com/NICourced/fontmaster

# Upstream git tags have no "v" prefix; the archive root is fontmaster-%version.
Source0: https://github.com/NICourced/fontmaster/archive/refs/tags/%version.tar.gz

BuildRequires: cmake >= 3.10
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: pkg-config
BuildRequires: libharfbuzz-devel >= 15.1
BuildRequires: libpng-devel
BuildRequires: libcairo-devel
BuildRequires: librsvg-devel >= 2.46
BuildRequires: libjpeg-turbo-devel >= 3.0
BuildRequires: libtiff-devel >= 4.5
BuildRequires: libxml2-devel
BuildRequires: zlib-devel
BuildRequires: qt5-base-devel
BuildRequires: desktop-file-utils

%description
FontMaster works directly with binary .ttf and .otf fonts, including color
emoji fonts. It can inspect and render glyphs, export PNG previews, replace
glyph artwork and save modified fonts.

This package contains the shared library. The command line tool is provided by
%name-cli, the Qt desktop application by %name-qt.

%package cli
Summary: Command line interface for FontMaster
Group: Graphics
Requires: %name = %EVR

%description cli
Command line interface for inspecting, rendering and editing compiled
OpenType fonts.

%package qt
Summary: Qt desktop application for FontMaster
Group: Graphics
Requires: %name = %EVR

%description qt
Qt desktop application for inspecting and editing fonts, built on top of the
FontMaster library.

%package devel
Summary: Development files for FontMaster
Group: Development/C++
Requires: %name = %EVR

%description devel
Headers and CMake package files for developing against the FontMaster
library.

%prep
%setup -q -n %name-%version

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_TESTING=OFF
%cmake_build

%install
%cmake_install
install -Dm644 packaging/fontmaster.desktop \
    %buildroot%_desktopdir/fontmaster.desktop
install -Dm644 packaging/fontmaster.svg \
    %buildroot%_iconsdir/hicolor/scalable/apps/fontmaster.svg

%check
desktop-file-validate %buildroot%_desktopdir/fontmaster.desktop || true

%files
%_libdir/libfontmaster.so.*
%_docdir/%name/

%files cli
%_bindir/fontmaster_cli

%files qt
%_bindir/fontmaster_qt
%_desktopdir/fontmaster.desktop
%_iconsdir/hicolor/scalable/apps/fontmaster.svg

%files devel
%_includedir/fontmaster/
%_libdir/libfontmaster.so
%_libdir/cmake/fontmaster/

%changelog
* Wed Nov 12 2026 Freeman3301 <freeman3301@users.noreply.github.com> 0.0.2-alt1
- Initial ALT build of FontMaster 0.0.2.
