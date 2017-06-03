import nengo
import nengo.spa as spa
import numpy as np

D = 256   # options: 64, 128, 256, 384, 512

D_space = 256  # options: 64, 128, 256, 384, 512

vocab_space = spa.Vocabulary(D_space)

model = spa.SPA()
with model:
    
    model.rule = spa.State(D_space, vocab=vocab_space)
    
    model.objs = spa.State(D_space, feedback=1, vocab=vocab_space)

    model.status = spa.State(32)
    
    speed = 0.3
    separation = 0.3
    strength = 0.4
    
    model.subjx = spa.Compare(D_space)
    model.subjy = spa.Compare(D_space)
    model.objx = spa.Compare(D_space)
    model.objy = spa.Compare(D_space)
    
    for ens in model.all_ensembles:
        ens.neuron_type = nengo.Direct()
    
    model.cortical = spa.Cortical(spa.Actions(
        'subjx_A=rule*~S*X',
        'subjy_A=rule*~S*Y',
        'objx_A=rule*~O*X',
        'objy_A=rule*~O*Y',
        'subjx_B=objs',
        'subjy_B=objs',
        'objx_B=objs',
        'objy_B=objs',
    ))        
    
    
    actions = spa.Actions(
        'dot(rule, (BELOW-ABOVE-LEFT-RIGHT)*V)*{strength} +'
        '(subjy - objy)+{separation} --> '
                 'status=BAD, '
                 'objs=-{speed}*Y*objs*~S + {speed}*Y*objs*~O'.format(**locals()),
        'dot(rule, (BELOW-ABOVE-LEFT-RIGHT)*V)*{strength} +'
        '(subjy - objy)-{separation} --> '
                  'status=GOOD'.format(**locals()),

        'dot(rule, (ABOVE-BELOW-LEFT-RIGHT)*V)*{strength} +'
        '(objy - subjy)+{separation} --> '
                 'status=BAD, '
                 'objs=-{speed}*Y*objs*~O + {speed}*Y*objs*~S'.format(**locals()),
        'dot(rule, (BELOW-ABOVE-LEFT-RIGHT)*V)*{strength} +'
        '(objy - subjy)-{separation} --> '
                  'status=GOOD'.format(**locals()),



    )
    
    def input(t):
        t = t % 0.8
        if t< 0.4:
            return 'OBJ1*S+ABOVE*V+OBJ2*O'
        else:
            return 'OBJ2*S+BELOW*V+OBJ1*O'
    
    model.input = spa.Input(rule=input)
    
    model.bg = spa.BasalGanglia(actions)
    
    model.thal = spa.Thalamus(model.bg)
    
    
    def display_node(t, x):
        return x
    
    display = nengo.Node(display_node, size_in=4)
    
    nengo.Connection(model.objs.output, display[0], 
              transform=[vocab_space.parse('OBJ1*X').v])
    nengo.Connection(model.objs.output, display[1], 
              transform=[vocab_space.parse('OBJ1*Y').v])
    nengo.Connection(model.objs.output, display[2], 
              transform=[vocab_space.parse('OBJ2*X').v])
    nengo.Connection(model.objs.output, display[3], 
              transform=[vocab_space.parse('OBJ2*Y').v])
              
              
              
              