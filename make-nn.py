#!/usr/bin/env python3

import sys

def run(struct):
    outlines = ['digraph g {']
    outlines += get_layer_nodes(1, struct[0], 'input')

    for layer_n, nodes_next in enumerate(struct[1:],2):
        lab = 'output' if layer_n == len(struct) else ''
        outlines += get_layer_nodes(layer_n, nodes_next, lab)

    n_nodes = struct[0]
    for layer_n, nodes_next in enumerate(struct[1:],1):
        outlines += get_connections(layer_n, n_nodes, nodes_next)
        n_nodes = nodes_next

    outlines += ['}']
    for line in outlines:
        print(line)


def get_layer_nodes(layer_n, n_nodes, label=''):
    out_list = []
    for noden in range(n_nodes):
        out_list.append(r'{x}{y} [label="{l}"]'.format(
                x=noden, y=layer_n, l=label))
    return out_list

def get_connections(layer_n, n_nodes, nodes_next):
    out_list = []
    for noden in range(n_nodes):
        in_name = '{x}{y}'.format(x=noden, y=layer_n)
        for outn in range(nodes_next):
            out_name = '{x}{y}'.format(x=outn, y=layer_n+1)
            out_list.append(in_name + ' -> ' + out_name)
    return out_list

if __name__ == '__main__':
    if len(sys.argv) == 0:
        sys.exit('usage: {} <nodes>...'.format(sys.argv[0]))
    struct = [int(x) for x in sys.argv[1:]]
    run(struct)
