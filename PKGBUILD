# Maintainer: Frederik Lind <email>
pkgname=games-tui
pkgver=1.0.0
pkgrel=1
pkgdesc="A collection of terminal based mini games"
arch=("any")
url="https://github.com/frederiklind/games-tui"
license=('MIT')
depends=('python' 'python-pip')
makedepends('python-setuptools')
source=('$pkgname-$pkgver.tar.gz::https://github.com/frederiklind/games-tui/archive/refs/tags/v$pkgver.tar.gz')
sha256sums=('SKIP') # IMPLEMENT THIS!

build() {

}

package() {
    cd "$srcdir/$pkgname-$pkgver"
    
    install -dm755 "$pkgdir/usr/bin"
    install -dm755 "$pkgdir/usr/share/$pkgname"

    cp -r app conf pyproject.toml setup.py ""
}
