const moment = require('moment');
const { summary } = require('@actions/core/lib/summary');

function createComment(results) {
   let message = `![2ms logo](https://github.com/Miguel-Neiva01/2ms-github-action/blob/main/images/2ms_icon.svg?raw=true)\n`;

    message += "\n| Repo | Total Items Scanned | Secrets Found | Test Passed |\n";
    message += "|------|---------------------|---------------|-------------|\n";  

    for (const [repo, data] of Object.entries(results)) {
        const testPassed = data.repo_scan ? "✅" : "❌";  
        message += `| ${repo} | ${data['total-items-scanned']} | ${data['total-secrets-found']} | ${testPassed} |\n`;
    }

    message += "\n";
    return message;
}

async function postJobSummary(results) {
    const message = createComment(results);

    console.log("Gerando Job Summary...");
    await summary.addRaw(message).write();
    console.log("Job Summary gerado com sucesso!");
}

module.exports = {
    postJobSummary
};
