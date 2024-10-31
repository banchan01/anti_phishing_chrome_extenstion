import * as onnx from 'onnxruntime-node';

let model = null;

async function loadModel() {
    try {
        model = await onnx.InferenceSession.create('./rf_model.onnx');
        console.log('Model loaded successfully');
    } catch (error) {
        console.error('Error loading model:', error);
        throw error;
    }
}

async function predictPhishing(features) {
    if (!model) {
        await loadModel();
    }

    try {
        // Convert features to array and ensure numeric values
        const featureValues = [
            features.length_url,
            features.length_hostname,
            features.ip,
            features.nb_dots,
            features.nb_hyphens,
            features.nb_qm,
            features.nb_and,
            features.nb_eq,
            features.nb_underscore,
            features.nb_percent,
            features.nb_slash,
            features.nb_semicolumn,
            features.nb_www,
            features.page_rank,
            features.google_index
        ].map(val => Number(val) || 0);

        // Create the input tensor
        const inputTensor = new onnx.Tensor('float32', featureValues, [1, 15]);

        // Run model with input tensor
        const outputs = await model.run({
            'float_input': inputTensor
        });

        // Get the prediction from output_label
        const prediction = outputs.output_label ? outputs.output_label.data[0] : 0;

        return prediction;
    } catch (error) {
        console.error('Prediction error:', error);
        throw error;
    }
}

export { loadModel, predictPhishing };