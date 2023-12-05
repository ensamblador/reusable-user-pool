
# Simple ECS Cluster Stack

Este proyecto crea los siguientes recursos dentro de una región de AWS:

* 1 User Pool
* Cognito domain 
* Usuarios por defecto (definidos en parameter store)
* Parámetros creados:
    * pool-id
    * custom-domain


La idea de este proyecto es contar con un pool de usuario para diferentes proyectos futuros. Solo agregndo nuevas apps (app id / app secret)



![user pool](/user-pool.jpg)

El codigo de la infra está en [`user_pool_stack.py`](user_pool/user_pool_stack.py)



## Instrucciones para despliegue


Clonar y crear un ambiente virtual python para el proyecto

```zsh
git clone https://github.com/ensamblador/reusable-user-pool.git
cd reusable-user-pool
python3 -m venv .venv
```

En linux o macos el ambiente se activa así:

```zsh
source .venv/bin/activate
```

en windows

```cmd
% .venv\Scripts\activate.bat
```

Una vez activado instalamos las dependencias
```zsh
pip install -r requirements.txt
```

en este punto ya se puede desplegar:

```zsh
cdk deploy
```

y para eliminar:

```zsh
cdk destroy
```


## Otros comandos útiles

 * `cdk synth`       crea un template de cloudformation con los recursos de este proyecto
 * `cdk diff`        compara el stack desplegado con el nuevo estado local

Enjoy!
