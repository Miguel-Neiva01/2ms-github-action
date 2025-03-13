const fs = require("fs");
const core = require("@actions/core");
const path = require("path");
const { postJobSummary } = require("./report");

async function run() {
  try {
    const resultsPath = path.join(process.cwd(), "results/results.json");

    console.log("Checking if the 'results.json' file exists...");

    if (!fs.existsSync(resultsPath)) {
      core.setFailed("Results file not found in 'results/' folder.");
      console.log("File 'results.json' not found.");
      return;
    }

    console.log("File 'results.json' found:", resultsPath);

    const results = JSON.parse(fs.readFileSync(resultsPath, "utf8"));

    console.log("Results content:", JSON.stringify(results, null, 2));

      // Check if results are null or undefined before calling postJobSummary
      if (!results || Object.keys(results).length === 0) {
        core.setFailed("Results data is invalid or empty.");
        return;
      }

    await postJobSummary(results);

  } catch (error) {
    core.setFailed(`Workflow error: ${error.message}`);
    console.error("Error during execution:", error);
  }
}

run();
