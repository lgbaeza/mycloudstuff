#based on a series
for i in {1..100}
do
       echo "Hola $i"
done

#based on a variable
length=100
for (( i = 1; i <= $length; i++ )) 
do
       echo "do something right $i times"
done