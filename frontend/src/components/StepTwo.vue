<template>
    <v-select multiple clearable :items="columns" label="Sélectionner les colonnes X"v-model="selectedColumnsX"></v-select>
    <v-select clearable :items="columns" label="Sélectionner la colonne Y" v-model="selectedColumnsY"></v-select>

    <v-btn @click="submitSelection">Confirm Selection !</v-btn>
    <v-btn @click="train_model">Lancer le training !</v-btn>
</template>

<script>
export default {
    props: {columns :[],fileName: ""},
    data() {
    return {
        selectedColumnsX: [],
        selectedColumnsY: [],
    }
},
    methods: {
        submitSelection() {
            this.$emit("selectedX", this.selectedColumnsX);
            this.$emit("selectedY", this.selectedColumnsY);
            console.log(this.fileName)
        },
        async train_model() {
            try {

                const response = await fetch("http://127.0.0.1:5000/train?"+
                'filename='+encodeURIComponent(this.fileName)+"&"+
                'colsX='+encodeURIComponent([...this.selectedColumnsX])+"&"+
                'colY='+encodeURIComponent( [this.selectedColumnsY]),
                {method: "GET", mode:'no-cors'}).then(response=>response.json()).then(response=>{console.log(response)});

                if (!response.ok) {
                    const errorData = await response.json();
                    console.error("Erreur traitement:", errorData);
                    return;
                }

                const data = await response.json();
                console.log("Model Trained successfully:", data);
                this.$emit("Trained", liste_indic);
            } catch (error) {
                console.error("model trained failed:", error);
            }
        }
        
    },
};
</script>