chmod -R 755 ./
dos2unix *.*
git add . -A
git commit -m 123
#git push -f Homenas pc:master
#git push -f Roomnas pc:master
git push -f USA $1:master
