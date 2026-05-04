# Proyecto Final AWS Data Engineering: Banking Transaction Pipeline 🚀

Proyecto de infraestructura como código usando **OpenTofu** para automatizar el despliegue de un pipeline serverless en AWS. Este proyecto implementa una lógica de procesamiento de transacciones bancarias utilizando AWS Step Functions y AWS Lambda, integrando prácticas de CI/CD mediante GitHub Actions.

> Desarrollado para el curso de **AWS Academy Data Engineering** — Universidad Autónoma de Guadalajara.

---

## 📐 Arquitectura del Pipeline

El pipeline procesa transacciones bancarias en formato JSON, evaluando su nivel de riesgo y enrutándolas a diferentes prefijos dentro de un bucket de S3.

El flujo es orquestado por **AWS Step Functions**:

```mermaid
graph TD
    A[Inicio: Evento JSON] --> B[L1: ValidateTransaction]
    B --> C[L2: AssessRisk]
    C --> D{Choice: risk_level}
    D -- "high" --> E[L3: RouteTransaction (review/)]
    D -- "low" --> F[L3: RouteTransaction (approved/)]
    E --> G[(S3 Bucket)]
    F --> G
```

1. **ValidateTransaction (L1)**: Verifica que la transacción tenga un monto mayor a 0, un código de país ISO de 2 letras y un formato de cuenta válido.
2. **AssessRisk (L2)**: Calcula el riesgo de la transacción. Se considera de alto riesgo (`risk_level: high`) si el monto supera los $10,000 o si el país de origen no es México ("MX").
3. **RouteTransaction (L3)**: Guarda el registro JSON procesado en el bucket S3 bajo el prefijo `approved/` (si es bajo riesgo) o `review/` (si es alto riesgo).

---

## 📂 Estructura del Proyecto

```
banking-pipeline-tofu/
├── .github/workflows/tofu.yml       # Flujo CI/CD automatizado
├── main.tf                          # S3, Lambdas y llamadas a módulos
├── step_function.tf                 # Definición ASL de la máquina de estados
├── iam.tf                           # Políticas de IAM (sin modificar)
├── variables.tf                     # Variables de entrada
├── lambdas/
│   ├── validate_json/lambda_function.py
│   ├── scan_content/lambda_function.py  # Reutilizado como L2 AssessRisk
│   └── route_file/lambda_function.py
├── tests/                           # Casos de prueba JSON
│   ├── normal_transaction.json
│   ├── high_amount_transaction.json
│   └── foreign_transaction.json
└── modules/lambda_function/         # Módulo reutilizable de Lambda
```

---

## ⚙️ CI/CD y Automatización

El despliegue de este proyecto está totalmente automatizado mediante **GitHub Actions** (`.github/workflows/tofu.yml`). 
Se utiliza **OIDC (OpenID Connect)** para autenticar GitHub con AWS sin necesidad de almacenar credenciales a largo plazo.

### Flujo de Trabajo (Workflow)
1. **Linting & Formatting**: Se verifica el formato del código de OpenTofu (`tofu fmt`).
2. **Plan**: Se genera un plan de ejecución detallado cuando hay Pull Requests hacia `main`.
3. **Apply**: Cuando se hace un merge o commit directo a `main`, se ejecuta `tofu apply -auto-approve` para desplegar la infraestructura en la nube.

---

## 🚀 Despliegue Local

### Prerrequisitos
- OpenTofu `>= 1.6`
- AWS CLI configurado
- Credenciales con permisos suficientes

### Comandos de uso

```bash
# Inicializar OpenTofu
tofu init

# Configurar la variable student_id (crear terraform.tfvars)
echo 'student_id = "12345"' > terraform.tfvars

# Visualizar cambios
tofu plan

# Desplegar en AWS
tofu apply -auto-approve
```

---

## 🔒 Casos de Prueba

La carpeta `tests/` incluye ejemplos listos para invocar la Step Function:
- **`normal_transaction.json`**: Monto $1500, MX. (Termina en `approved/`)
- **`high_amount_transaction.json`**: Monto $25000, MX. (Termina en `review/`)
- **`foreign_transaction.json`**: Monto $500, US. (Termina en `review/`)
