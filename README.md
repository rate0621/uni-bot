# bot-on-line

名前の通り、基本的にくだらないことばかりの機能

## デプロイ方法
毎回忘れるのでメモ

### cloneしてくる

`git clone --recursive https://github.com/rate0621/bot-on-line.git`

※submoduleを使っているため、--recursiveを付与

### submoduleを最新化させる
`git submodule foreach git pull origin master`

### herokuへpush

通常であればgitへのpushをフックして、herokuへデプロイできるが、
herokuの都合でsubmoduleを使っているとデプロイができない。
というわけで直接herokuへデプロイする。

`git push https://git.heroku.com/uni-bot-py.git master`


