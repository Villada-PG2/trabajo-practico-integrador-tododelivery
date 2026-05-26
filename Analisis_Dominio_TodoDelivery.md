# Dominio Todo Delivery
Todo Delivery es un negocio de elaboración y venta de comidas rápidas, con servicio de entrega a
domicilio. Este emprendimiento solamente admite pedidos telefónicos por parte de sus clientes,
no se realizan ventas en mostrador. El área de cobertura para el reparto, son los barrios de la zona
sur de la ciudad.
Este negocio ha solicitado el diseño e implementación de un sistema de información
que le permita gestionar el proceso de toma de pedido, elaboración y entrega del mismo al cliente.
Luego de realizar un relevamiento, se obtuvo la siguiente información y consideraciones para
construir el sistema.
Cuando el cliente se comunica, la telefonista atiende la consulta de los productos
según su tipo e informa los precios.
El negocio vende diferentes tipos de productos: sándwiches, lomos, pizzas, empanadas, minutas,
ensaladas, bebidas. Cada tipo agrupa distintos productos, cada uno con su precio. Por ejemplo:

El cliente realiza el pedido a la telefonista, quien anota cada uno de los productos
solicitados. Luego de informar el monto total, el cliente indica el domicilio de entrega y con cuánto
dinero abonará, para determinar si se le entrega cambio al repartidor.
En el pedido se anota el número de pedido, la fecha y hora de solicitud, nombre y
apellido del cliente, número de teléfono, domicilio de entrega completo, cada uno de los
productos solicitados y la cantidad asociada, importe de cada producto, importe total, con cuánto
dinero abonará el cliente y demora estimada informada.
La telefonista deja el duplicado del pedido en una pila, ordenando el mismo según el
orden de pedido. En la cocina se toma el pedido y se elabora el mismo. Finalizada la
elaboración, los productos son ubicados en las cajas o envoltorios correspondientes y el
responsable de cocina entrega los productos elaborados al responsable de entregas para su
control.

El responsable de entregas arma el pedido según lo definido, con los productos
provenientes de la cocina y las bebidas, en caso de que corresponda. En ese momento se escribe
en alguno de los envoltorios el domicilio de entrega. Una vez armado el pedido, se genera el ticket
requerido para efectuar el cobro al cliente. Se definió que el nuevo sistema deberá imprimir los
tickets utilizando una impresora fiscal, en un tiempo nunca superior a 5 segundos.
El pedido se entrega al repartidor, junto con el ticket y el dinero en cambio para el
vuelto, en caso de ser necesario. El responsable de entregas anota en el pedido el
repartidor asignado al mismo.
Cuando el pedido es entregado en el domicilio, el repartidor recibe el dinero y
entrega el ticket y el dinero por el vuelto, si corresponde. Al regresar al negocio, el repartidor
entrega el dinero cobrado por cada uno de los pedidos entregados al responsable de entregas,
quien realiza el control del dinero recibido. Si existe alguna diferencia, el responsable de entregas
registra la situación para su análisis posterior al finalizar el día. En ambos casos (existe o no
diferencia en la rendición del repartidor), el responsable de entregas registra la recepción de
dinero y actualiza los pedidos indicando que fue entregado al cliente.
En forma semanal, se elabora el listado de productos vendidos, con la cantidad de
cada producto vendido en la semana y el importe que representa en la facturación total, a fin de
definir nuevas estrategias para la publicidad de los productos y estrategias de venta.
Periódicamente se definen los precios de los productos, los cuales son consultados
por la telefonista al momento de atender al cliente y al calcular el monto total del pedido.
Por otra parte, el responsable de compras define la mercadería necesaria para la
elaboración de los productos y las bebidas a adquirir a los distintos proveedores.
Los pedidos se toman hasta 30 minutos antes de horario de cierre del negocio. Cada repartidor
puede realizar como máximo 3 entregas que no superen un monto de $20000.
El nuevo sistema contará con pantallas táctiles en la cocina, que permitirán que el
responsable de cocina visualice los pedidos en el orden que se registran, pueda consultar el detalle
de los mismos y registrar la finalización de la elaboración.
Se acordó con los responsables del negocio que el sistema deberá tener pantallas
similares a las de Windows.

## Reglas de negocio:
* **Exclusividad de canal:** Solo se admiten pedidos telefónicos por parte de los clientes; no se realizan ventas en mostrador bajo ninguna circunstancia.
* **Zona de cobertura:** El reparto de los pedidos se limita estrictamente a los barrios de la zona sur de la ciudad.
* **Horario de corte:** Los pedidos telefónicos se aceptan y registran hasta un máximo de 30 minutos antes del horario de cierre del negocio.
* **Restricción de despacho por repartidor:** Cada repartidor puede realizar como máximo 3 entregas simultáneas por viaje, y el monto de dicho conjunto de entregas no debe superar los $20000.
* **Impresión fiscal obligatoria:** El sistema debe emitir y procesar los tickets requeridos para el cobro utilizando obligatoriamente una impresora fiscal.
* **Tiempo límite de facturación:** El proceso de impresión de los tickets fiscales en el nuevo sistema nunca debe ser superior a los 5 segundos.
* **Interfaz de usuario:** El diseño de las pantallas del sistema de información debe ser similar al entorno visual de Windows.

## Objetivo:
Gestionar los procesos de consulta de productos y precios, toma de pedidos telefónicos, visualización y control de elaboración en cocina, armado, asignación de repartos, rendición de dinero de los repartidores y generación de estadísticas de facturación semanal para el negocio Todo Delivery.

## Entradas:
* Datos del cliente (nombre, apellido, teléfono, domicilio completo).
* Detalles del pedido (productos seleccionados, cantidades asociadas, monto con el que abona).
* Actualizaciones periódicas de precios de los productos.
* Registro de finalización de elaboración de productos (desde la pantalla táctil de cocina).
* Asignación de repartidores a los pedidos correspondientes.
* Dinero rendido por el repartidor y datos de control de caja (registro de diferencias).
* Definición de mercadería y bebidas necesarias informadas por el responsable de compras.

## Salidas:
* Información de productos y precios en pantalla para la telefonista.
* Importe total calculado del pedido y monto estimado del cambio/vuelto.
* Visualización ordenada del listado y detalle de pedidos en las pantallas táctiles de la cocina.
* Ticket fiscal impreso a través de la impresora fiscal.
* Listado semanal de productos vendidos (cantidades acumuladas e importe de participación en la facturación total).
* Registro de novedades de diferencias de caja detectadas en la rendición diaria.

## Frontera:
* La preparación física y cocción de los alimentos en la cocina.
* El traslado físico de los pedidos por parte de los repartidores hacia los domicilios de los clientes.
* La adquisición real y negociación de mercadería y bebidas con los proveedores (el sistema solo contempla la definición de necesidades por el responsable de compras).
* El análisis e investigación profunda de las diferencias de dinero al final del día (el sistema solo se limita a registrar la situación de discrepancia detectada en la rendición).

## Entorno:
* Clientes
* Telefonista
* Responsable de cocina
* Responsable de entregas
* Repartidores
* Responsable de compras
* Proveedores

## Alcance:

### 1. Gestión de Productos y Precios
* **1.1** El sistema debe permitir la consulta de productos organizados por su tipo (sándwiches, lomos, pizzas, empanadas, minutas, ensaladas y bebidas) junto con sus respectivos precios vigentes.
* **1.2** Debe permitir registrar y actualizar de forma periódica los precios asignados a cada uno de los productos del negocio.

### 2. Gestión y Registro de Pedidos
* **2.1** El sistema debe permitir registrar los datos completos de un pedido telefónico: número de pedido, fecha y hora de solicitud, nombre y apellido del cliente, número de teléfono, domicilio de entrega completo, productos solicitados y la cantidad asociada a cada uno.
* **2.2** Debe calcular automáticamente el importe de cada producto y el importe total del pedido en función de las cantidades y los precios vigentes.
* **2.3** El sistema debe registrar el monto con el que abonará el cliente y calcular el dinero en cambio (vuelto) que se le debe entregar al repartidor.
* **2.4** Debe permitir el ingreso y registro de la demora estimada informada al cliente al momento de consolidar la comunicación.

### 3. Control y Monitoreo de Elaboración en Cocina
* **3.1** El sistema debe desplegar los pedidos en las pantallas táctiles de la cocina, listados estrictamente bajo el orden en que fueron registrados.
* **3.2** Debe permitir al responsable de cocina consultar el detalle específico de cualquiera de los pedidos en espera o en preparación.
* **3.3** El sistema debe permitir al responsable de cocina registrar la finalización de la elaboración de los productos correspondientes a un pedido para habilitar su posterior control y armado.

### 4. Armado, Facturación y Despacho de Pedidos
* **4.1** El sistema debe facilitar el control del armado del pedido (productos de cocina combinados con las bebidas correspondientes).
* **4.2** Debe generar y ordenar la impresión automatizada del ticket fiscal de cobro a través de la impresora fiscal en un tiempo no mayor a 5 segundos.
* **4.3** El sistema debe permitir registrar la asignación del repartidor al pedido, verificando que no se violen los límites máximos permitidos (hasta 3 entregas que no superen un monto de $20000).

### 5. Rendición de Cuentas y Cierre de Pedidos
* **5.1** El sistema debe permitir registrar la recepción del dinero cobrado por el repartidor al regresar al negocio.
* **5.2** Debe permitir el registro de las situaciones en las que se detecten diferencias o discrepancias entre el dinero recibido y el ticket emitido, guardando la información para su posterior análisis al finalizar el día.
* **5.3** El sistema debe actualizar el estado del pedido, marcándolo formalmente como "entregado al cliente" una vez procesada la rendición de dinero (exista o no diferencia).

### 6. Reportes y Publicidad
* **6.1** El sistema debe generar de forma semanal el listado de productos vendidos, detallando la cantidad total de cada producto comercializado en la semana y el importe exacto que representa dentro de la facturación total, con el fin de asistir en la definición de estrategias de venta y publicidad.

## R.N.F.:
* **Hardware de Cocina:** El sistema debe operar en pantallas táctiles ubicadas en el área de la cocina para la visualización y actualización de pedidos.
* **Hardware de Salida:** Interfaz e integración obligatoria con una impresora fiscal para la emisión de los tickets de cobro.
* **Eficiencia de Tiempo:** La generación e impresión del ticket fiscal debe completarse en un tiempo estricto nunca superior a los 5 segundos.
* **Interfaz de Usuario (Look & Feel):** El sistema debe contar con interfaces gráficas y pantallas con un diseño similar al entorno de Windows.