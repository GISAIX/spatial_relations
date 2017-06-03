import nengo
import nengo.spa as spa

D = 32

model = spa.SPA()
with model:
    
    model.rule = spa.State(D)
    
    model.obj1 = spa.State(1, feedback=1)
    
    model.obj2 = spa.State(1, feedback=1)
    
    model.status = spa.State(D)
    
    actions = spa.Actions(
        'dot(rule, OBJ1*S+LEFT*V+OBJ2*O)*0.4 + (dot(obj1, X) - dot(obj2, X))+0.3 --> status=BAD, obj1=-0.1*X, obj2=0.1*X',
        'dot(rule, OBJ1*S+LEFT*V+OBJ2*O)*0.4 - (dot(obj1, X) - dot(obj2, X))-0.3 --> status=GOOD',
    )
    
    model.input = spa.Input(rule='OBJ1*S+LEFT*V+OBJ2*O')
    
    model.bg = spa.BasalGanglia(actions)
    
    model.thal = spa.Thalamus(model.bg)
    