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
import IntControl from 'scripts/lib/workflows/controls/IntControl';
import Node from 'scripts/lib/workflows/Node.vue';

export default class IntComponent extends Rete.Component {
  constructor(numSocket) {
    super('Integer');
    this.componentType = 'SourceNode';
    this.numSocket = numSocket;
    this.data.component = Node;
  }

  builder(node) {
    const out1 = new Rete.Output('num', 'Integer', this.numSocket);
    node.componentType = this.componentType;
    node.nodeDescription = 'Source data type Integer';

    return node
      .addControl(new IntControl(this.editor, 'num'))
      .addOutput(out1);
  }

  /* eslint-disable class-methods-use-this */
  worker(node, inputs, outputs) {
    outputs.num = node.data.num;
  }
  /* eslint-enable class-methods-use-this */
}
