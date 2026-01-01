# Ejemplo de Uso de Agents en MenuLab

Este documento explica cómo usar los "agents" (workflows automatizados) de MenuLab para generar menús digitales automáticamente.

## ¿Qué son los Agents?

Los agents en MenuLab son workflows automatizados de GitHub Actions que generan menús digitales personalizados basados en los datos del cliente. Estos workflows se activan mediante eventos `repository_dispatch` y procesan la información para crear un sitio web completo con el menú del negocio.

## Planes Disponibles

MenuLab ofrece 4 planes diferentes, cada uno con características específicas:

| ID Plan | Nombre | Descripción |
|---------|--------|-------------|
| 0 | Plan Base | Menú online gratuito con hasta 25 ítems |
| 1 | Plan Emprendedor | Menú imprimible + edición en Google Sheets |
| 2 | Plan Profesional | Menú imprimible + online + código QR |
| 3 | Plan Corporativo | Todas las características + reservas + pedidos web |

## Cómo Disparar un Agent

### Opción 1: Usando la API de GitHub (Recomendado)

Puedes disparar un agent enviando un evento `repository_dispatch` a través de la API de GitHub:

```bash
curl -X POST \
  https://api.github.com/repos/CHM5/MenuLab/dispatches \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer TU_TOKEN_DE_GITHUB" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -d '{
    "event_type": "generar_menu_profesional",
    "client_payload": {
      "plan": "2",
      "email": "cliente@ejemplo.com",
      "nombreCompleto": "Juan Pérez",
      "negocio": "RestauranteDemo",
      "external_reference": "REF-12345",
      "sheet_url": "https://docs.google.com/spreadsheets/d/TU_SHEET_ID/edit"
    }
  }'
```

### Opción 2: Usando JavaScript/Node.js

Si estás integrando MenuLab en tu aplicación Node.js:

```javascript
const axios = require('axios');

async function generarMenu(datosCliente) {
  const response = await axios.post(
    'https://api.github.com/repos/CHM5/MenuLab/dispatches',
    {
      event_type: determinarEventType(datosCliente.plan),
      client_payload: {
        plan: datosCliente.plan,
        email: datosCliente.email,
        nombreCompleto: datosCliente.nombreCompleto,
        negocio: datosCliente.negocio,
        external_reference: datosCliente.external_reference,
        sheet_url: datosCliente.sheet_url
      }
    },
    {
      headers: {
        'Accept': 'application/vnd.github+json',
        'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`,
        'X-GitHub-Api-Version': '2022-11-28'
      }
    }
  );
  
  return response.data;
}

function determinarEventType(planId) {
  const eventos = {
    '0': 'generar_menu_base',
    '1': 'generar_menu_emprendedor',
    '2': 'generar_menu_profesional',
    '3': 'generar_menu_corporativo'
  };
  return eventos[planId];
}

// Ejemplo de uso
generarMenu({
  plan: '2',
  email: 'cliente@ejemplo.com',
  nombreCompleto: 'María González',
  negocio: 'CafeteriaEjemplo',
  external_reference: 'MP-ORDER-456',
  sheet_url: 'https://docs.google.com/spreadsheets/d/ABC123/edit'
})
.then(() => console.log('Menú generado exitosamente'))
.catch(error => console.error('Error:', error));
```

### Opción 3: Usando Python

Para aplicaciones Python:

```python
import requests
import os

def generar_menu(datos_cliente):
    """
    Dispara el workflow de generación de menú
    
    Args:
        datos_cliente (dict): Diccionario con los datos del cliente
    """
    event_types = {
        '0': 'generar_menu_base',
        '1': 'generar_menu_emprendedor',
        '2': 'generar_menu_profesional',
        '3': 'generar_menu_corporativo'
    }
    
    url = 'https://api.github.com/repos/CHM5/MenuLab/dispatches'
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {os.environ["GITHUB_TOKEN"]}',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    
    payload = {
        'event_type': event_types[datos_cliente['plan']],
        'client_payload': datos_cliente
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    
    return response.status_code == 204  # GitHub devuelve 204 en éxito

# Ejemplo de uso
cliente = {
    'plan': '3',
    'email': 'chef@restaurante.com',
    'nombreCompleto': 'Carlos Rodríguez',
    'negocio': 'LaParrilla',
    'external_reference': 'ORD-789',
    'sheet_url': 'https://docs.google.com/spreadsheets/d/XYZ789/edit'
}

if generar_menu(cliente):
    print('✓ Workflow disparado exitosamente')
else:
    print('✗ Error al disparar el workflow')
```

## Estructura del client_payload

El `client_payload` debe contener los siguientes campos:

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `plan` | string | Sí | ID del plan: "0", "1", "2", o "3" |
| `email` | string | Sí | Email del cliente (para enviar el menú) |
| `nombreCompleto` | string | Sí | Nombre completo del cliente |
| `negocio` | string | Sí | Nombre del negocio (usado para carpetas/URLs) |
| `external_reference` | string | Sí | Referencia externa (ej: ID de pago de MercadoPago) |
| `sheet_url` | string | Sí | URL completa de Google Sheets con los datos del menú |

## Tipos de Eventos Disponibles

Los siguientes event_types están disponibles:

- `generar_menu_base` - Genera un menú del Plan Base (Plan 0)
- `generar_menu_emprendedor` - Genera un menú del Plan Emprendedor (Plan 1)
- `generar_menu_profesional` - Genera un menú del Plan Profesional (Plan 2)
- `generar_menu_corporativo` - Genera un menú del Plan Corporativo (Plan 3)

## Qué Hace el Agent

Cuando se dispara un agent, el workflow ejecuta los siguientes pasos:

1. **Clona el repositorio** - Obtiene el código más reciente
2. **Extrae los datos del cliente** - Lee el payload enviado
3. **Configura Python** - Instala las dependencias necesarias
4. **Lee Google Sheets** - Conecta con la hoja de cálculo del cliente
5. **Genera el sitio** - Ejecuta el script Python correspondiente al plan
6. **Commit y push** - Guarda el menú generado en el repositorio
7. **Genera código QR** - Crea un código QR para el menú (planes 1+)
8. **Envía email** - Envía confirmación al cliente con los enlaces
9. **Guarda referencias** - Almacena los enlaces en la base de datos

## Ejemplo Completo de Integración

Aquí hay un ejemplo completo de cómo integrar MenuLab en un sistema de pagos:

```javascript
// Webhook de MercadoPago u otro procesador de pagos
app.post('/webhook/pago-confirmado', async (req, res) => {
  const { payment_id, external_reference, payer_email } = req.body;
  
  // 1. Obtener datos del pedido desde tu base de datos
  const pedido = await obtenerPedidoPorReferencia(external_reference);
  
  // 2. Crear Google Sheet para el cliente
  const sheetUrl = await crearGoogleSheetParaCliente(pedido.negocio);
  
  // 3. Disparar generación de menú
  await generarMenu({
    plan: pedido.planId.toString(),
    email: payer_email,
    nombreCompleto: pedido.nombreCliente,
    negocio: pedido.nombreNegocio,
    external_reference: external_reference,
    sheet_url: sheetUrl
  });
  
  res.status(200).send('OK');
});
```

## Tiempo de Procesamiento

El workflow típicamente tarda entre **2-4 minutos** en completarse:

- Setup inicial: ~30 segundos
- Procesamiento de datos: ~30-60 segundos
- Generación del sitio: ~30-60 segundos
- Commit y push: ~10-20 segundos
- Espera de propagación: ~90 segundos
- Envío de email: ~10 segundos

## Resultado

Una vez completado el workflow:

1. El cliente recibe un email con:
   - ✅ Link al menú online
   - ✅ Link a su Google Sheet para editar
   - ✅ Código QR (para planes 1+)
   - ✅ Código de descuento (para planes 1-3)

2. El menú queda disponible en: `https://menulab.com.ar/menu/{negocio}/`

3. Los datos se guardan en la hoja de "Clientes" para referencia futura

## Consideraciones de Seguridad

- 🔒 Nunca expongas tu `GITHUB_TOKEN` en el código del frontend
- 🔒 Usa variables de entorno para almacenar credenciales
- 🔒 Valida los datos del cliente antes de disparar el workflow
- 🔒 Implementa rate limiting para evitar abusos

## Troubleshooting

### El workflow no se dispara

- Verifica que el token de GitHub tenga permisos de `repo` y `workflow`
- Confirma que el `event_type` coincida con los definidos en el workflow
- Revisa que todos los campos del `client_payload` estén presentes

### El email no llega

- Verifica que el email en el payload sea válido
- Revisa la carpeta de spam del destinatario
- Confirma que los secrets SMTP estén configurados correctamente

### El sitio no se genera

- Verifica que la URL de Google Sheet sea correcta y esté compartida con la service account
- Revisa los logs del workflow en GitHub Actions
- Confirma que el plan enviado sea válido ("0", "1", "2", o "3")

## Soporte

Para más información o soporte, contacta al equipo de MenuLab.
