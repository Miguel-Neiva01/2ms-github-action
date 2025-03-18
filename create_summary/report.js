const { summary } = require('@actions/core/lib/summary');

function createComment(results) {
   let message = `![2ms logo](https://github.com/Miguel-Neiva01/2ms-github-action/blob/main/images/2ms_icon.svg?raw=true)\n`;

    message += "\n| Repo | Secrets Found | Different Results | Test Passed | Execution Time |\n";
    message += "|------|---------------|-------------------|-------------|----------------|\n";  

    for (const [repo, data] of Object.entries(results)) {
        const totalSecretsFound = data['total_secrets_found'] || 0;
        const testPassed = data.repo_scan ? "✅" : "❌";
        const differentResults = data['different_results'] || 0;  
        const executionTime = data['execution_time'] ? `${data['execution_time']} ms` : 'N/A';  
        
        message += `| ${repo} | ${totalSecretsFound} | ${differentResults} | ${testPassed} | ${executionTime} |\n`;
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
