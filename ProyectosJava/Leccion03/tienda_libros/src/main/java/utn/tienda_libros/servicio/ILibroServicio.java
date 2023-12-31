package utn.tienda_libros.servicio;

import utn.tienda_libros.modelo.Libro;

import java.util.List;

public interface ILibroServicio {

    public List <Libro> listarLibros();
    public Libro buscarLibroPorId(Integer idLibro);
    public void guardarLibro(Libro Libro);
    public void eliminarLibro(Libro Libro);
}
