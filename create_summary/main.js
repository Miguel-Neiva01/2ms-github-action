const fs = require("fs");
const core = require("@actions/core");
const path = require("path");
const { postJobSummary } = require("./report");

async function run() {
  try {
    const resultsPath = path.join(process.cwd(), "results/results.json");

    if (!fs.existsSync(resultsPath)) {
      core.setFailed("Results file not found in 'results/' folder.");
      return;
    }

 
    await postJobSummary();

  } catch (error) {
    core.setFailed(`Workflow error: ${error.message}`);
  }
}

run();
