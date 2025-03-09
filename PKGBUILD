# Maintainer: Frederik Lind <frederik.lind.mail@proton.me>

pkgname=games-tui
pkgver=1.0.0
pkgrel=1
pkgdesc="A collection of terminal based mini-games"
arch=(x86_64)
url="https://github.com/frederiklind/games-tui"
license=('MIT')
depends=()
makedepends=(git python)
optdepends=()
provides=(games-tui)
source=("git+$url")
sha256sums=()
validpgpkeys=('7220E7839C1D2816')

prepare() {
	cd "$pkgname-$pkgver"
	patch -p1 -i "$srcdir/$pkgname-$pkgver.patch"
}

build() {
	cd "$pkgname-$pkgver"
	./configure --prefix=/usr
	make
}

check() {
	cd "$pkgname-$pkgver"
	make -k check
}

package() {
	cd "$pkgname-$pkgver"
	make DESTDIR="$pkgdir/" install
}
