/* Copyright 2020 Karlsruhe Institute of Technology
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. */

import Rete from 'rete';
import NumControl from 'scripts/lib/workflows/controls/NumControl';
import Node from 'scripts/lib/workflows/Node.vue';

export default class AddComponent extends Rete.Component {
  constructor(numSocket) {
    super('Add');
    this.numSocket = numSocket;
    this.data.component = Node;
  }

  builder(node) {
    const inp1 = new Rete.Input('num1', 'Number', this.numSocket);
    const inp2 = new Rete.Input('num2', 'Number', this.numSocket);
    const out = new Rete.Output('result', 'Number', this.numSocket);

    inp1.addControl(new NumControl(this.editor, 'num1'));
    inp2.addControl(new NumControl(this.editor, 'num2'));

    return node
      .addInput(inp1)
      .addInput(inp2)
      .addControl(new NumControl(this.editor, 'show_sum', true))
      .addOutput(out);
  }

  worker(node, inputs, outputs) {
    const n1 = inputs.num1.length ? inputs.num1[0] : node.data.num1;
    const n2 = inputs.num2.length ? inputs.num2[0] : node.data.num2;
    const sum = n1 + n2;

    this.editor.nodes
      .find((n) => n.id === node.id).controls.get('show_sum').setValue(sum);
    outputs.result = sum;
  }
}
