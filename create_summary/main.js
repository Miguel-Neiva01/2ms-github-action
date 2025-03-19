const fs = require("fs");
const core = require("@actions/core");
const path = require("path");
const { postJobSummary } = require("./report");

async function run() {
  try {
    const resultsPath = path.join(process.cwd(), "app/results/results.json");

    console.log("Checking if the 'results.sarif' file exists...");

    if (!fs.existsSync(resultsPath)) {
      core.setFailed("Results file not found in 'results/' folder.");
      console.log("File 'results.sarif' not found.");
      return;
    }

    console.log("File 'results.json' found:", resultsPath);

  
    const results = JSON.parse(fs.readFileSync(resultsPath, "utf8"));

    await postJobSummary(results); 

  } catch (error) {
    core.setFailed(`Workflow error: ${error.message}`);
    console.error("Error during execution:", error);
  }
}

run();
