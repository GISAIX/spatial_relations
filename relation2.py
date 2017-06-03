import nengo
import nengo.spa as spa

D = 256

D_space = 256
vocab_space = spa.Vocabulary(D_space)

model = spa.SPA()
with model:
    
    model.rule = spa.State(D)
    
    model.objs = spa.State(D_space, feedback=1, vocab=vocab_space)
    
    model.status = spa.State(D)
    
    actions = spa.Actions(
        'dot(rule, OBJ1*BELOW*V+OBJ2*O)*0.4 +'
        '(dot(objs, OBJ1*Y) - dot(objs, OBJ2*Y))+0.5 --> '
                 'status=BAD, '
                 'objs=-0.1*Y*OBJ1 + 0.1*Y*OBJ2',
        'dot(rule, OBJ1*S+BELOW*V+OBJ2*O)*0.4 - '
        
        '(dot(objs, OBJ1*Y) - dot(objs, OBJ2*Y))-0.5 --> '
                  'status=GOOD',
        
        'dot(rule, OBJ1*S+LEFT*V+OBJ2*O)*0.4 +'
        '(dot(objs, OBJ1*X) - dot(objs, OBJ2*X))+0.3 --> '
                 'status=BAD, '
                 'objs=-0.1*X*OBJ1 + 0.1*X*OBJ2',
        'dot(rule, OBJ1*S+LEFT*V+OBJ2*O)*0.4 - '
        
        '(dot(objs, OBJ1*X) - dot(objs, OBJ2*X))-0.3 --> '
                  'status=GOOD',
                  
    )
    
    def input(t):
        t = t % 0.8
        if t< 0.4:
            return 'OBJ1*S+BELOW*V+OBJ2*O'
        else:
            return 'OBJ1*S+LEFT*V+OBJ2*O'
    
    model.input = spa.Input(rule=input)
    
    model.bg = spa.BasalGanglia(actions)
    
    model.thal = spa.Thalamus(model.bg)
    