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
import TextControl from 'scripts/lib/workflows/controls/TextControl';
import Node from 'scripts/lib/workflows/components/Node.vue';

export default class AddStringComponent extends Rete.Component {
  constructor(strSocket) {
    super('AddString');
    this.strSocket = strSocket;
    this.data.component = Node;
  }

  builder(node) {
    const inp1 = new Rete.Input('str1', 'String', this.strSocket);
    const inp2 = new Rete.Input('str2', 'String', this.strSocket);
    const out = new Rete.Output('result', 'String', this.strSocket);

    inp1.addControl(new TextControl(this.editor, 'str1'));
    inp2.addControl(new TextControl(this.editor, 'str2'));

    return node
      .addInput(inp1)
      .addInput(inp2)
      .addControl(new TextControl(this.editor, 'show_sum'))
      .addOutput(out);
  }

  worker(node, inputs, outputs) {
    const n1 = inputs.str1.length ? inputs.str1[0] : node.data.str1;
    const n2 = inputs.str2.length ? inputs.str2[0] : node.data.str2;
    const sum = n1 + n2;

    this.editor.nodes
      .find((n) => n.id === node.id).controls.get('show_sum').setValue(sum);
    outputs.result = sum;
  }
}
