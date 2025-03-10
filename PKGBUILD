# Maintainer: Frederik Lind <frederik.lind.mail@proton.me>

pkgname=games-tui
pkgver=1.0.0
pkgrel=1
pkgdesc="A collection of terminal based mini-games"
arch=(x86_64)
url="https://github.com/frederiklind/games-tui"
license=('MIT')
depends=(python)
makedepends=(git python python-pip python-virtualenv pyinstaller)
optdepends=()
provides=(games-tui)
source=("git+$url")
sha256sums=()
validpgpkeys=('7220E7839C1D2816')

pkgver() {
  cd "$pkgname"
  git describe --tags --abbrev=0 | sed 's/^v//'
}

build() {
	cd "$pkgname"

  # setup venv
  python -m venv .venv
  .venv/bin/pip install --upgrade pip
  .venv/bin/pip install -r requirements.txt
  .venv/bin/pip install pyinstaller

	# compile
  .venv/bin/pyinstaller --onefile --name $pkgname src/games_tui/main.py
}

package() {
  cd "$pkgname"
  
  install -Dm755 "dist/$pkgname" "$pkgdir/usr/bin/$pkgname"
  
  install -Dm755 -d "$pkgdir/usr/share/$pkgname/config"
  cp -r config/* "$pkgdir/usr/share/$pkgname/config/"
  
  install -Dm755 -d "$pkgdir/usr/share/$pkgname/data"
  cp -r data/* "$pkgdir/usr/share/$pkgname/data/"
  
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}

post_install() {
  APP_NAME="games-tui"
  USER_CONFIG_DIR="$HOME/.config/$APP_NAME"
  USER_DATA_DIR="$HOME/.local/share/$APP_NAME"

  # create dirs
  mkdir -p "$USER_CONFIG_DIR"
  mkdir -p "$USER_DATA_DIR"

  # copy files
  cp -n "/usr/share/$APP_NAME/config/"* "$USER_CONFIG_DIR/"
  cp -n "/usr/share/$APP_NAME/data/"* "$USER_DATA_DIR/"

  echo "Default configuration and data files have been copied to:"
  echo "  - $USER_CONFIG_DIR"
  echo "  - $USER_DATA_DIR"
}
