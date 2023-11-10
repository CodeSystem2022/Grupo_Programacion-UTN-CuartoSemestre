// this === global = true

//Mostrar algo en consola
//console.log();

//Mostrar un mensaje en forma de error
//console.error();

//Ejecutar un codigo despues de un intervalo de tiempo 
//setTimeout(()=>{});

//Ejecutar un codigo cada intervalo de tiempo
//setInterval(()=>{});

//da prioridad de ejecicion a una función asincronica
//setImmdiate(()=>{});

//console.log(setInterval);

let i = 0;
let intervalo = setInterval(()=> {
//    console.log("Hola");
   if (i===3){
        clearInterval(intervalo);    
   }
    i++;
},1000);

setImmediate(()=>{
    console.log('Saludos inmediato');
})

//requiere();

console.log(__filename);
