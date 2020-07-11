set -x

tar xzf tmux_config.tar.gz
cp -R tmux_config ~
cd ~
mv tmux_config .tmux

#cd ~
#git clone https://github.com/gpakosz/.tmux.git
ln -s $HOME/.tmux/.tmux.conf
cp $HOME/.tmux/.tmux.conf.local $HOME
