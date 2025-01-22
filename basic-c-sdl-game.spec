Name: basic-c-sdl-game
Version: 1.0
Release: alt1
Summary: A basic SDL game in C
License: MIT
Group: Games/Arcade
Url: https://github.com/aminosbh/basic-c-sdl-game
Source: %{name}-%{version}.tar.gz
Packager: Sergey Sychkin <serezha.sych.00@gmail.com>

BuildRequires: git build-essential pkg-config cmake cmake-data libsdl2-dev libsdl2-gfx-dev libsdl2-image-dev libsdl2-ttf-dev libsdl2-net-dev libsdl2-mixer-dev
%description
A basic SDL game written in C. It uses SDL2 for rendering graphics.

%prep
%setup -q

%build
mkdir build
cd build
cmake ..
make

%install
mkdir -p %{buildroot}/usr/games
mkdir -p %{buildroot}/usr/share/applications

install -m 755 basic-c-sdl-game %{buildroot}/usr/games/basic-c-sdl-game

cat > %{buildroot}/usr/share/applications/basic-c-sdl-game.desktop << EOF
[Desktop Entry]
Name=Basic SDL Game
Exec=/usr/games/basic-c-sdl-game
Type=Application
Categories=Game;
EOF

%files
/usr/games/basic-c-sdl-game
/usr/share/applications/basic-c-sdl-game.desktop

%changelog
* Mon Jan 22 2025 Your Name <your.email@example.com> 1.0-alt1
- Initial ALT Linux package.
