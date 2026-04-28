# demo-tofu 🚀

Proyecto de demostración de infraestructura como código usando **OpenTofu** (fork open-source de Terraform) para desplegar un pipeline serverless de procesamiento y cuarentena de archivos en AWS.

> Desarrollado para el curso de **Big Data** — UAG.

---

## 📐 Arquitectura

El proyecto despliega un pipeline de tres pasos orquestado por funciones Lambda que valida, escanea y enruta archivos entrantes a un bucket S3:

```
Evento de entrada
      │
      ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   validate  │────▶│     scan     │────▶│    route    │
│  (Lambda 1) │     │  (Lambda 2)  │     │  (Lambda 3) │
└─────────────┘     └──────────────┘     └─────────────┘
  Valida campos       Detecta firma         Mueve archivo a:
  obligatorios        EICAR (malware)       • clean/
                                            • quarantine/
                                                  │
                                                  ▼
                                          ┌──────────────┐
                                          │  S3 Bucket   │
                                          │  (quarantine)│
                                          └──────────────┘
```

---

## 📁 Estructura del proyecto

```
demo-tofu/
├── main.tf                          # Recursos principales (S3 + módulos Lambda)
├── iam.tf                           # Rol IAM y políticas para las Lambdas
├── variables.tf                     # Definición de variables de entrada
├── outputs.tf                       # Outputs del proyecto
├── terraform.tfvars                 # Valores de variables (no versionado)
├── .gitignore
│
├── lambdas/
│   ├── validate_json/
│   │   └── lambda_function.py       # Paso 1: Valida campos obligatorios
│   ├── scan_content/
│   │   └── lambda_function.py       # Paso 2: Escanea por firma EICAR
│   └── route_file/
│       └── lambda_function.py       # Paso 3: Enruta a clean/ o quarantine/
│
└── modules/
    └── lambda_function/
        ├── main.tf                  # Módulo reutilizable: empaqueta y despliega Lambda
        ├── variables.tf
        └── outputs.tf
```

---

## ☁️ Recursos AWS desplegados

| Recurso | Nombre | Descripción |
|---|---|---|
| `aws_s3_bucket` | `{project_name}-{student_id}` | Bucket principal de almacenamiento |
| `aws_lambda_function` | `...-validate` | Valida el esquema del evento de entrada |
| `aws_lambda_function` | `...-scan` | Detecta contenido malicioso (firma EICAR) |
| `aws_lambda_function` | `...-route` | Mueve el archivo a la carpeta correcta en S3 |
| `aws_iam_role` | `...-lambda-role` | Rol compartido por las tres Lambdas |
| `aws_iam_policy` | `...-s3-access` | Permisos `GetObject`, `PutObject`, `DeleteObject` sobre el bucket |

---

## ⚙️ Variables

| Variable | Tipo | Default | Descripción |
|---|---|---|---|
| `project_name` | `string` | `"curso-tofu"` | Prefijo usado en el nombre de todos los recursos |
| `student_id` | `string` | *(requerido)* | Identificador único del estudiante |
| `aws_region` | `string` | `"us-east-1"` | Región de AWS donde se despliega la infraestructura |

---

## 📤 Outputs

| Output | Descripción |
|---|---|
| `bucket_name` | Objeto completo del bucket S3 creado |
| `bucket_arn` | ARN del bucket S3 |

---

## 🔧 Lambdas — Lógica de negocio

### 1. `validate_json`
Verifica que el evento de entrada contenga todos los campos obligatorios:

```
file_id · filename · bucket · input_key · content_base64
```

Si falta alguno, lanza un `ValueError`. Si pasa, añade `validation_passed: true` al evento y lo retorna.

---

### 2. `scan_content`
Decodifica el campo `content_base64` y busca la firma **EICAR** (estándar para pruebas de antivirus):

- ✅ Limpio → `is_malicious: false`, `scan_reason: "clean"`
- 🚨 Detectado → `is_malicious: true`, `scan_reason: "EICAR signature detected"`

---

### 3. `route_file`
Lee el flag `is_malicious` del evento y copia el archivo dentro del bucket S3:

- Limpio → `s3://<bucket>/clean/<file_id>.json`
- Malicioso → `s3://<bucket>/quarantine/<file_id>.json`

El archivo de origen se elimina después de la copia.

---

## 🏗️ Módulo reutilizable: `lambda_function`

El módulo `./modules/lambda_function` encapsula el patrón de despliegue de cualquier Lambda Python:

1. Empaqueta automáticamente el directorio fuente en un `.zip` usando `archive_file`.
2. Despliega la función con runtime `python3.12`.
3. Calcula el hash del código para detectar cambios en re-despliegues.

**Variables del módulo:**

| Variable | Tipo | Default | Descripción |
|---|---|---|---|
| `function_name` | `string` | — | Nombre de la función Lambda |
| `source_dir` | `string` | — | Ruta al directorio con el código Python |
| `role_arn` | `string` | — | ARN del rol IAM a asignar |
| `timeout` | `number` | `10` | Timeout en segundos |

---

## 🚀 Uso

### Prerrequisitos

- [OpenTofu](https://opentofu.org/docs/intro/install/) `>= 1.6`
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) configurado (`aws configure`)
- Credenciales AWS con permisos sobre S3, Lambda e IAM

### Configuración

Crea un archivo `terraform.tfvars` (no se versiona):

```hcl
student_id = "tu-id-aqui"
```

### Comandos

```bash
# 1. Inicializar providers y módulos
tofu init

# 2. Previsualizar los cambios
tofu plan

# 3. Desplegar la infraestructura
tofu apply

# 4. Destruir todos los recursos
tofu destroy
```

---

## 🔒 Seguridad y buenas prácticas

- `terraform.tfvars` está en `.gitignore` — los valores sensibles nunca se versionan.
- El estado de Terraform (`*.tfstate`) tampoco se versiona — usar un backend remoto (S3 + DynamoDB) en producción.
- El rol IAM sigue el principio de **mínimo privilegio**: solo acceso a los objetos del bucket propio del proyecto.

---

## 📝 Licencia

Proyecto académico — UAG Big Data.
