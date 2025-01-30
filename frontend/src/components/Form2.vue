<template>
    <v-form v-model="isValid" ref="form">
        <v-container>
            <v-row>
                <v-col cols="12" md="6">
                    <v-select
                        multiple
                        clearable
                        :items="availableColumnsX"
                        label="Sélectionner les colonnes X"
                        v-model="selectedColumnsX"
                        @update:modelValue="handleInput1Change"
                        :rules="[rules.required]">
                    </v-select>
                </v-col>
                <v-col cols="12" md="6">
                    <v-select
                        clearable
                        :items="availableColumnsY"
                        label="Sélectionner la colonne Y"
                        v-model="selectedColumnsY"
                        @update:modelValue="handleInput2Change"
                        :rules="[rules.required]">
                    </v-select>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12">
                    <v-data-table
                        :headers="previewHeaders"
                        :items="preview"
                        item-value="name"
                        class="elevation-1">
                    </v-data-table>
                </v-col>
            </v-row>
            <v-btn @click="submitSelection" items="fileName">Confirm Selection</v-btn>
        </v-container>
    </v-form>
</template>

<script>
export default {
    props: ["columnsForm2", "preview", "fileName"],
    data() {
        return {
            isValid: false,
            selectedColumnsX: [],
            selectedColumnsY: [],
            rules: {
                required: (value) => !!value || 'Ce champ est requis',
            }
        };
    },
    computed: {
        availableColumnsX() {
            return this.columnsForm2.filter(col => !this.selectedColumnsY.includes(col));
        },
        availableColumnsY() {
            return this.columnsForm2.filter(col => !this.selectedColumnsX.includes(col));
        },
        previewHeaders() {
            return this.preview.length > 0 ? Object.keys(this.preview[0]).map(key => ({ text: key, value: key })) : [];
        }
    },
    methods: {
        submitSelection(items) {
            this.$emit("selected", this.selectedColumnsX, this.selectedColumnsY, this.fileName);
        },
        async validateForm() {
            console.log("validateForm()")
            const valid = this.selectedColumnsX.length > 0 && this.selectedColumnsY.length > 0;
            this.$emit("form2ValidateEmit", valid);
        },
        handleInput1Change(event) {
            console.log("handleInput1Change()")
            this.selectedColumnsX = event;
            this.validateForm();
        },
        handleInput2Change(event) {
            console.log("handleInput2Change()")
            this.selectedColumnsY = event;
            this.validateForm();
        }
    }
}
</script>
