from datetime import date, time, datetime
from pydantic import ValidationError

from modelos import (
    TipoProducto, Proveedor, Mercaderia, Producto, Envoltorio, 
    DetallePedido, Cliente, Ticket, Pedido, Reparto, 
    Telefonista, Repartidor, ResponsableEntregas, ControlDinero,
    ResponsableCocina, ImpresoraFiscal, ListadoSemanalVentas, DetalleListadoVentas
)

def main():
    print("SISTEMA TODO DELIVERY")

    telefonista = Telefonista(nombre="María Gonzalez")
    repartidor = Repartidor(nombre="Andrés López")
    responsable_cocina = ResponsableCocina(nombre="Carlos Chef")
    responsable_entregas = ResponsableEntregas(nombre="Roberto Sanchez")
    impresora = ImpresoraFiscal()

    prov_bebidas = Proveedor(nombre="Distribuidora Sur S.A.")
    prov_fiambres = Proveedor(nombre="Fiambrería El Sol")
    
    merc_coca = Mercaderia(descripcion="Coca Cola 1.5L", proveedores=[prov_bebidas])
    merc_muzzarella = Mercaderia(descripcion="Queso Muzzarella", proveedores=[prov_fiambres])

    tipo_pizza = TipoProducto(nombre="Pizzas")
    tipo_bebida = TipoProducto(nombre="Bebidas")

    prod_pizza = Producto(
        nombre="Pizza Especial", 
        precio=8500.0, 
        tipo_producto=tipo_pizza, 
        mercaderias=[merc_muzzarella]
    )
    
    prod_coca = Producto(
        nombre="Coca Cola", 
        precio=1500.0, 
        tipo_producto=tipo_bebida, 
        mercaderias=[merc_coca]
    )

    cliente_santiago = Cliente(nombre="Santiago", apellido="Ayerra", telefono=3511234567) 

    print("\nCASO 1: Creación de Pedido Válido")
    try:
        detalle1 = DetallePedido(cantidadAsociada=2, importeProducto=17000.0, producto=prod_pizza)
        detalle2 = DetallePedido(cantidadAsociada=1, importeProducto=1500.0, producto=prod_coca)
        env = Envoltorio(domicilioEscrito="Av. Velez Sarsfield 1500, B° Sur")

        pedido_valido = Pedido(
            numeroPedido=101,
            fechaSolicitud=date.today(),
            horaSolicitud=time(20, 30),
            domicilioEntregaCompleto="Av. Velez Sarsfield 1500",
            importeTotal=18500.0,
            montoAbonar=20000.0,
            vuelto=1500.0,
            demoraEstimadaInformada=time(21, 15),
            estado="Pendiente",
            cliente=cliente_santiago,
            detalles=[detalle1, detalle2],
            envoltorios=[env]
        )
        print(f"Pedido N°{pedido_valido.numeroPedido} creado exitosamente para {pedido_valido.cliente.nombre} {pedido_valido.cliente.apellido}.")
        
    except ValidationError as e:
        print("Error al crear el pedido válido:")
        print(e)

    print("\nCASO 2: Validación Cruzada")
    try:
        pedido_invalido = Pedido(
            numeroPedido=102,
            fechaSolicitud=date.today(),
            horaSolicitud=time(20, 45),
            domicilioEntregaCompleto="San Martin 300",
            importeTotal=5000.0,
            montoAbonar=6000.0,
            vuelto=500.0,  #ERROR INTENCIONAL
            demoraEstimadaInformada=time(21, 30),
            estado="Pendiente",
            cliente=cliente_santiago,
            detalles=[detalle2],
            envoltorios=[env]
        )
    except ValidationError as e:
        print("Pydantic atrapó el error correctamente:")
        for error in e.errors():
            print(f"  -> {error['msg']}")

    print("\nCASO 3: Reparto excede monto máximo")
    try:
        pedido_grande = Pedido(
            numeroPedido=103,
            fechaSolicitud=date.today(),
            horaSolicitud=time(21, 00),
            domicilioEntregaCompleto="Belgrano 10",
            importeTotal=5000.0,
            montoAbonar=5000.0,
            vuelto=0.0,
            demoraEstimadaInformada=time(21, 40),
            estado="Preparado",
            cliente=cliente_santiago,
            detalles=[detalle2],
            envoltorios=[env]
        )
        reparto_invalido = Reparto(pedidos=[pedido_valido, pedido_grande])
    except ValidationError as e:
        print("Pydantic atrapó la regla de negocio del Reparto:")
        for error in e.errors():
            print(f"  -> {error['msg']}")

    print("\nCASO 4: Inconsistencias lógicas")
    try:
        reparto_valido = Reparto(pedidos=[pedido_grande])
        control = ControlDinero(
            dineroEntregado=4000.0,
            diferencia=-1000.0,
            existeDiferencia=False, # ERROR INTENCIONAL
            responsable_control=responsable_entregas,
            reparto=reparto_valido
        )
    except ValidationError as e:
        print("Pydantic detectó la inconsistencia en el Control de Dinero:")
        for error in e.errors():
            print(f"  -> {error['msg']}")


    # PRUEBA DE METODOS

    print("\nCASO 5: Prueba de Metodos")

    cliente_santiago.RealizarPedido()
    telefonista.atenderConsulta()
    telefonista.informarPrecios()
    telefonista.tomarPedido(pedido_valido)

    print("\nEl pedido pasa a cocina...")
    responsable_cocina.visualizarPedidos([pedido_valido])
    responsable_cocina.consultarDetalle(pedido_valido)
    responsable_cocina.registrarFinalizacionElaboracion(pedido_valido)
    
    print("\nEl pedido pasa al área de entregas...")
    responsable_entregas.armarPedido(pedido_valido)
    nuevo_ticket = responsable_entregas.generarTicket(pedido_valido)
    impresora.imprimirTicket(nuevo_ticket)
    responsable_entregas.asignarRepartidor(pedido_valido, repartidor.nombre)

    print("\nEl repartidor sale a la calle...")
    repartidor.entregarPedido(pedido_valido)
    dinero_recibido_cliente = repartidor.cobrar(pedido_valido)
    vuelto_entregado = repartidor.entregarVuelto(pedido_valido)
    print(f"Cobrado al cliente: ${dinero_recibido_cliente} | Vuelto entregado: ${vuelto_entregado}")
    responsable_entregas.actualizarPedidoEntregado(pedido_valido)

    print("\nEl repartidor regresa y rinde el dinero...")
    dinero_rendido = repartidor.rendirDinero(dinero_recibido_cliente)
    diferencia = responsable_entregas.controlarDineroRecibido(montoEsperado=pedido_valido.importeTotal, montoRecibido=(dinero_rendido - vuelto_entregado))
    
    if diferencia == 0:
        responsable_entregas.registrarRecepcionDinero()
    else:
        responsable_entregas.registrarDiferencia(diferencia)

    print(f"\n[ESTADO FINAL] El pedido N°{pedido_valido.numeroPedido} finalizó con estado: '{pedido_valido.estado}'.")

    print("CASO 6: Generacion de Listados")
    
    det_venta_pizza = DetalleListadoVentas(
        cantidadVendidaSemana=45, 
        importeFacturacionTotal=(45 * prod_pizza.precio), 
        producto=prod_pizza
    )
    det_venta_coca = DetalleListadoVentas(
        cantidadVendidaSemana=60, 
        importeFacturacionTotal=(60 * prod_coca.precio), 
        producto=prod_coca
    )

    reporte_semanal = ListadoSemanalVentas(
        semana=date.today(),
        detalles=[det_venta_pizza, det_venta_coca]
    )
    reporte_semanal.generarListado()

if __name__ == "__main__":
    main()