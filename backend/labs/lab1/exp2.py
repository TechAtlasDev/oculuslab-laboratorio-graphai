from app.services.optimus_service import OptimusService
import json

optimuskg = OptimusService()
nodo = optimuskg.get_node_by_label("GEN", random=True)

print (json.dumps(nodo, indent=4))