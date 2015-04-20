#!/usr/bin/env python3
"""Script to make graphviz NN graphs"""


import sys
import argparse
import itertools

_autoencoder_start = [
    'subgraph cluster_a { ',
    'color=red',
    'penwidth=4']

_output_color = 'orange'

def _z(num):
    return '" "'
    # return '<Z<SUB>{}</SUB>>'.format(num)

def run(args):
    struct = args.nodes
    outlines = [
        'digraph g {',
        # 'splines=false'
    ]
    outlines += get_layer_nodes(
        1, struct[0], ['input'], color='green')#, boxframe='white', box='white')
    layers = len(struct)

    for layer_n, nodes_next in enumerate(struct[1:],2):
        lab = [_z(layer_n)]
        color = 'white'
        if layer_n == layers and not args.autoencoder:
            lab = args.out_layer
            color = _output_color
        outlines += get_layer_nodes(layer_n, nodes_next, lab, color=color)

    if args.autoencoder:
        lab = [_z(layers - 1)]
        outlines += get_layer_nodes(
            layers + 1, struct[-2], lab, color=_output_color)

    n_nodes = struct[0]
    for layer_n, nodes_next in enumerate(struct[1:],1):
        train = (args.autoencoder and layer_n == layers - 1) or args.train
        outlines += get_connections(
            layer_n, n_nodes, nodes_next, backprop=args.backprop, train=train)
        n_nodes = nodes_next

    if args.autoencoder:
        outlines += get_connections(
            layers, struct[-1], struct[-2], train=True)

    outlines += ['}']
    for line in outlines:
        print(line)

def _opts(opts):
    return ', '.join(['{} = {}'.format(k,v) for k,v in opts.items()])

def get_layer_nodes(layer_n, n_nodes, labels=[''], box=None, color='white',
                    boxframe='black'):
    out_list = []
    if box:
        out_list += [
            'subgraph cluster{} {{'.format(layer_n),
            'style=filled',
            'fillcolor={}'.format(box),
            'color={}'.format(boxframe),
        ]
    for noden, label in zip(range(n_nodes), itertools.cycle(labels)):
        out_list.append(
            r'{x}{y} [label={l}, style=filled, fillcolor={c}]'.format(
                x=noden, y=layer_n, l=label, c=color))
    if box:
        out_list.append('}')
    return out_list

def get_connections(layer_n, n_nodes, nodes_next, backprop=False,
                    train=False):
    options = {
        'dir': 'back' if backprop else 'forward',
        'color':'red' if backprop or train else 'black',
    }
    if train:
        options['dir'] = 'both'
    if backprop and layer_n == 1:
        options['style'] = 'invisible'
        options['dir'] = 'none'
    out_list = []
    for noden in range(n_nodes):
        in_name = '{x}{y}'.format(x=noden, y=layer_n)
        for outn in range(nodes_next):
            out_name = '{x}{y}'.format(x=outn, y=layer_n+1)
            conex = '{} -> {} [{}]'.format(
                in_name, out_name, _opts(options))
            out_list.append(conex)
    return out_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('nodes', nargs='+', type=int)
    parser.add_argument('--out-layer', nargs='+', default=['output'])
    parser.add_argument('-b','--backprop', action='store_true')
    parser.add_argument('-a','--autoencoder', action='store_true')
    parser.add_argument('-t','--train', action='store_true')
    args = parser.parse_args()
    run(args)
