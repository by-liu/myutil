set -x

tar xzf bundle.tar.gz
mkdir -p $HOME/.vim
cp -R bundle $HOME/.vim
mkdir -p $HOME/.vim/colors
cp solarized.vim $HOME/.vim/colors
cp vimrc $HOME/.vimrc
cp vundle_vimrc $HOME
