async function analyzeWithAI() {
    const review = document.getElementById("review").value.trim();
    const result = document.getElementById("ai-result");
    const button = document.getElementById("ai-button");

    if (!review) {
        result.textContent = "Please enter a guest review.";
        return;
    }

    button.disabled = true;
    button.textContent = "Analyzing...";
    result.textContent = "AI is analyzing the review...";

    try {
        const response = await fetch("/api/ai/analyze", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({review})
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Request failed");
        }

        result.textContent = data.result;
    } catch (error) {
        result.textContent = "Unable to analyze the review right now.";
    } finally {
        button.disabled = false;
        button.textContent = "Analyze with AI";
    }
}
