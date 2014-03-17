<?php

/*

Script de AJAX para el control del color de los monitores, para la foto de
http://drmad.org/blog/fotografia-foreveralone.html

Por Oliver Etchebarne / Paperclip X10
http://drmad.org / http://x10.pe

*/

session_start() ;

// No hay ningun tipo de verificación. En $m se guarda el monitor que estamos
// modificando
$m = $_POST['m'];

// Aquí están los IPs de cada monitor.
$IPS = [
    0 => '192.168.1.10',
    1 => '192.168.1.11',
];

// Si no hay almacenado en la sesión información del color de este monitor...
if ( !isset ( $_SESSION['colors'][ $m ] )) {
    // ...empezamos todo en cero.
    $colors = [
        'R' => 0,
        'G' => 0,
        'B' => 0,
        'I' => 127,
    ];
}   
else {
    // De lo contrario, la recabamos
    $colors = $_SESSION['colors'][ $m ];
}

// Buscamos qué color estamos cambiando en esta llamada AJAX, y modificamos
// el array $colors
foreach ( ['R', 'G', 'B', 'I'] as $c ) {
    if ( isset ( $_POST [ $c ] ) ) {
        $colors [ $c ] =  $_POST [ $c ];
    }
}

// Convertimos todos los valores a hexadecimal
$str_c = '';
foreach ( $colors as $c ) {
    if ( $c > 255 ) $c = 255;

    $str_c .= str_pad ( dechex ( $c ), 2, '0', STR_PAD_LEFT );
}   

// Un fin de línea
$str_c .= "\n";


// Y lo enviamos al equipo correspondiente.
$s = socket_create ( AF_INET, SOCK_DGRAM, SOL_UDP );
socket_sendto ( $s, $str_c, strlen ( $str_c ) , 0 , $IPS[ $m ], 1922 ); 

// Guardamos en la sesión los cambios.
$_SESSION ['colors'][ $m ]  = $colors;
