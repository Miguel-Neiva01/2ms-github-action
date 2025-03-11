const moment = require('moment');
const { summary } = require('@actions/core/lib/summary');

function createComment(results) {
    let message = `\n**2ms version: ${results['version']}**\n`;  

    // Criação da tabela em Markdown
    message += "\n| Repo | Total Items Scanned | Test Passed |\n";
    message += "|------|---------------------|-------------|\n";  // Linha de separação

    // Adiciona cada repositório e o status do scan
    for (const [repo, data] of Object.entries(results)) {
        const testPassed = data.repo_scan ? "✅" : "❌";  // Usa um símbolo para mostrar se passou ou falhou
        message += `| ${repo} | ${data['total-items-scanned']} | ${testPassed} |\n`;
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
