<template>
    <div>
        <v-btn color="primary" @click="trainModel">Train Model</v-btn>
        <div v-if="accuracy !== null">
            <h3>Model Accuracy:</h3>
            <p>{{ accuracy }}</p>
            <p>{{ visuel }}</p>
        </div>
    </div>
</template>

<script>
export default {
    props: ["visuel"],
    data() {
        return {
            accuracy: null,
        };
    },
    methods: {
        async trainModel() {
            try {
                const response = await fetch("/api/train", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ columns: this.selectedColumns })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    console.error("Model training failed:", errorData);
                    return;
                }

                const data = await response.json();
                this.accuracy = data.accuracy;
            } catch (error) {
                console.error("Model training failed:", error);
            }
        },
    },
};
</script>
