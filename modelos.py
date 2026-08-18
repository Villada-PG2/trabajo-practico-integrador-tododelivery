from pydantic import BaseModel, Field, model_validator
from datetime import date, time, datetime
from typing import List, Optional

class TipoProducto(BaseModel):
    nombre: str = Field(..., min_length=2, description="Nombre del tipo de producto (ej: Pizza, Bebida)")

class Proveedor(BaseModel):
    nombre: str = Field(..., min_length=2, description="Nombre del proveedor")

class Mercaderia(BaseModel):
    descripcion: str = Field(..., min_length=3, description="Descripción de la mercadería")
    proveedores: List[Proveedor] = Field(..., min_length=1, description="Lista de proveedores de esta mercadería")

class Producto(BaseModel):
    nombre: str = Field(..., description="Nombre del producto")
    precio: float = Field(..., gt=0, description="El precio del producto debe ser estrictamente positivo")
    
    tipo_producto: TipoProducto = Field(..., description="Tipo al que pertenece el producto")
    mercaderias: List[Mercaderia] = Field(default_factory=list, description="Mercaderías necesarias para elaborar el producto")

class Envoltorio(BaseModel):
    domicilioEscrito: Optional[str] = Field(default=None, description="Domicilio escrito en el envoltorio (si aplica)")

class DetallePedido(BaseModel):
    cantidadAsociada: int = Field(..., gt=0, description="Cantidad del producto solicitado")
    importeProducto: float = Field(..., ge=0, description="Importe de este detalle")
    
    producto: Producto = Field(..., description="Producto que compone el detalle")

class Cliente(BaseModel):
    nombre: str = Field(..., min_length=2, description="Nombre del cliente")
    apellido: str = Field(..., min_length=2, description="Apellido del cliente")
    telefono: int = Field(..., gt=0, description="Número de teléfono de contacto")

    def RealizarPedido(self):
        print(f"El cliente {self.nombre} {self.apellido} está realizando un pedido telefónico.")

class Ticket(BaseModel):
    fechaHora: datetime = Field(..., description="Fecha y hora de emisión del ticket")
    montoTotal: float = Field(..., ge=0, description="Monto total del ticket a cobrar")

class ImpresoraFiscal(BaseModel):
    tiempoImpresionMaxSegundos: int = Field(default=5, frozen=True, description="Tiempo máximo para imprimir ticket")

    def imprimirTicket(self, ticket: Ticket):
        print("################ TICKET ###################")
        print(f"Fecha y Hora: {ticket.fechaHora}")
        print(f"Total a pagar: ${ticket.montoTotal}")
        print("###########################################")

class Pedido(BaseModel):
    numeroPedido: int = Field(..., gt=0, description="Número de identificación del pedido")
    fechaSolicitud: date = Field(..., description="Fecha en la que el cliente solicitó el pedido")
    horaSolicitud: time = Field(..., description="Hora de la solicitud")
    domicilioEntregaCompleto: str = Field(..., min_length=4, description="Dirección completa de entrega")
    importeTotal: float = Field(..., ge=0, description="Suma total a cobrar por los productos")
    montoAbonar: float = Field(..., ge=0, description="Dinero con el que abonará el cliente")
    vuelto: float = Field(..., ge=0, description="Vuelto calculado para el cliente")
    demoraEstimadaInformada: time = Field(..., description="Tiempo de demora informada al cliente")
    estado: str = Field(..., description="Estado actual del pedido (ej. Pendiente, En Preparación, Entregado)")

    cliente: Cliente = Field(..., description="Cliente que hizo el pedido")
    detalles: List[DetallePedido] = Field(..., min_length=1, description="Líneas de detalle del pedido")
    envoltorios: List[Envoltorio] = Field(..., min_length=1, description="Cajas o envoltorios del pedido")
    ticket: Optional[Ticket] = Field(default=None, description="Ticket emitido para este pedido")

    @model_validator(mode='after')
    def validar_calculos_dinero(self):
        """Validación Cruzada: Asegura que la matemática del cobro sea correcta."""
        if self.montoAbonar < self.importeTotal:
            raise ValueError("El monto a abonar no puede ser inferior al importe total del pedido.")
        
        # Validamos que el vuelto declarado coincida exactamente con la resta
        if self.vuelto != (self.montoAbonar - self.importeTotal):
            raise ValueError("Inconsistencia: El vuelto no coincide con la diferencia entre el monto abonado y el total.")
        return self

class Reparto(BaseModel):
    MAX_ENTREGAS: int = Field(default=3, frozen=True)
    MAX_MONTO: float = Field(default=20000.0, frozen=True)
    
    pedidos: List[Pedido] = Field(..., description="Lista de pedidos asignados a este viaje")

    @model_validator(mode='after')
    def validar_reglas_dominio_reparto(self):
        """Validación Cruzada: Verifica los límites de entregas y montos establecidos por el negocio."""
        if not (1 <= len(self.pedidos) <= self.MAX_ENTREGAS):
            raise ValueError(f"Violación de regla: Un reparto debe llevar entre 1 y {self.MAX_ENTREGAS} pedidos.")
        
        monto_total_reparto = sum(pedido.importeTotal for pedido in self.pedidos)
        if monto_total_reparto > self.MAX_MONTO:
            raise ValueError(f"Violación de regla: El monto total del reparto (${monto_total_reparto}) supera el límite permitido (${self.MAX_MONTO}).")
        
        return self

class Empleado(BaseModel):
    nombre: str = Field(..., min_length=2, description="Nombre del empleado")

class Telefonista(Empleado):
    pedidos_tomados: List[Pedido] = Field(default_factory=list)

    def atenderConsulta(self):
        print(f"[{self.nombre}] Atendiendo consulta telefónica del cliente...")

    def informarPrecios(self):
        print(f"[{self.nombre}] Informando los precios vigentes de los productos.")

    def tomarPedido(self, pedido: Pedido):
        self.pedidos_tomados.append(pedido)
        print(f"[{self.nombre}] Pedido N°{pedido.numeroPedido} registrado con éxito.")

class ResponsableCocina(Empleado):
    pedidos_elaborados: List[Pedido] = Field(default_factory=list)

    def visualizarPedidos(self, pedidos_pendientes: List[Pedido]):
        print("--- PANTALLA TÁCTIL: PEDIDOS PENDIENTES ---")
        for ped in pedidos_pendientes:
            if ped.estado != "Elaborado":
                print(f"Pedido N°{ped.numeroPedido} - Estado: {ped.estado}")

    def consultarDetalle(self, pedido: Pedido):
        print(f"--- DETALLES DEL PEDIDO N°{pedido.numeroPedido} ---")
        for detalle in pedido.detalles:
            print(f"- {detalle.cantidadAsociada}x {detalle.producto.nombre}")

    def registrarFinalizacionElaboracion(self, pedido: Pedido):
        pedido.estado = "Elaborado"
        self.pedidos_elaborados.append(pedido)

class ResponsableCompras(Empleado):
    mercaderias_gestionadas: List[Mercaderia] = Field(default_factory=list)

    def definirMercaderia(self, mercaderia: Mercaderia):
        self.mercaderias_gestionadas.append(mercaderia)

class ResponsableEntregas(Empleado):
    
    def armarPedido(self, pedido: Pedido):
        pedido.estado = "Armado"

    def generarTicket(self, pedido: Pedido):
        nuevo_ticket = Ticket(fechaHora=datetime.now(), montoTotal=pedido.importeTotal)
        pedido.ticket = nuevo_ticket
        return nuevo_ticket

    def asignarRepartidor(self, pedido: Pedido, repartidor_nombre: str):
        pedido.estado = "En viaje"
        print(f"Pedido asignado al repartidor: {repartidor_nombre}")

    def controlarDineroRecibido(self, montoEsperado: float, montoRecibido: float):
        diferencia = montoRecibido - montoEsperado
        return diferencia

    def registrarRecepcionDinero(self):
        print("Recepción del dinero del reparto registrada correctamente en el sistema.")

    def registrarDiferencia(self, diferencia: float):
        print(f"ATENCIÓN: Se ha registrado una diferencia de caja de ${diferencia}.")

    def actualizarPedidoEntregado(self, pedido: Pedido):
        pedido.estado = "Entregado"

class ControlDinero(BaseModel):
    dineroEntregado: float = Field(..., ge=0, description="Dinero total que rinde el repartidor")
    diferencia: float = Field(..., description="Diferencia de caja detectada (positiva o negativa)")
    existeDiferencia: bool = Field(..., description="Indica si se encontró un faltante o sobrante")
    
    responsable_control: ResponsableEntregas = Field(..., description="Responsable que realiza la rendición de caja")
    reparto: Reparto = Field(..., description="Reparto al que corresponde la rendición")

    @model_validator(mode='after')
    def validar_coherencia_diferencia(self):
        """Validación Cruzada: Coherencia lógica entre la bandera booleana y el monto de diferencia."""
        if self.diferencia != 0 and not self.existeDiferencia:
            raise ValueError("Error lógico: Si la diferencia no es 0, 'existeDiferencia' debe ser True.")
        if self.diferencia == 0 and self.existeDiferencia:
            raise ValueError("Error lógico: Si la diferencia es 0, 'existeDiferencia' debe ser False.")
        return self

class Repartidor(Empleado):
    repartos: List[Reparto] = Field(default_factory=list, description="Repartos efectuados por el repartidor")
    controles_dinero: List[ControlDinero] = Field(default_factory=list, description="Controles de rendición asociados al repartidor")

    def entregarPedido(self, pedido: Pedido):
        pedido.estado = "En domicilio"

    def cobrar(self, pedido: Pedido):
        return pedido.montoAbonar

    def entregarVuelto(self, pedido: Pedido):
        return pedido.vuelto

    def rendirDinero(self, dinero_entregado: float):
        return dinero_entregado

class DetalleListadoVentas(BaseModel):
    cantidadVendidaSemana: int = Field(..., ge=0, description="Unidades totales vendidas del producto")
    importeFacturacionTotal: float = Field(..., ge=0, description="Porcentaje o monto total dentro de la facturación")
    
    producto: Producto = Field(..., description="Producto reportado")

class ListadoSemanalVentas(BaseModel):
    semana: date = Field(..., description="Fecha (semana) a la que corresponde el reporte")
    detalles: List[DetalleListadoVentas] = Field(..., min_length=1, description="Detalle del listado")

    def generarListado(self):
        print(f"################ LISTADO SEMANAL DE VENTAS ({self.semana}) ###################")
        for detalle in self.detalles:
            print(f"Producto: {detalle.producto.nombre} | Vendidos: {detalle.cantidadVendidaSemana} | Recaudado: ${detalle.importeFacturacionTotal}")
        print("##############################################################################")