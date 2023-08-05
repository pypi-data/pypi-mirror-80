<!-- Copyright 2020 Karlsruhe Institute of Technology
   -
   - Licensed under the Apache License, Version 2.0 (the "License");
   - you may not use this file except in compliance with the License.
   - You may obtain a copy of the License at
   -
   -     http://www.apache.org/licenses/LICENSE-2.0
   -
   - Unless required by applicable law or agreed to in writing, software
   - distributed under the License is distributed on an "AS IS" BASIS,
   - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   - See the License for the specific language governing permissions and
   - limitations under the License. -->

<template>
  <div class="form-check">
    <input class="form-check-input" type="checkbox" v-model="checked" style="vertical-align: middle">
    <label class="form-check-label"></label>
  </div>
</template>

<script>

export default {
  props: {
    emitter: Object,
    ikey: String,
    getData: Function,
    putData: Function,
    defaultValue: Boolean,
    readonly: Boolean,
  },
  data() {
    return {
      checked: this.initial || false,
    };
  },
  watch: {
    checked() {
      this.update();
    },
  },
  methods: {
    update() {
      if (this.ikey) {
        this.putData(this.ikey, this.checked);
      }
      this.emitter.trigger('process');
    },
  },
  mounted() {
    this.checked = this.getData(this.ikey) || this.defaultValue;
    if (this.ikey) {
      this.putData(this.ikey, this.checked);
    }
  },
};
</script>
