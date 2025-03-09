const moment = require('moment');
const { summary } = require('@actions/core/lib/summary');

function createComment(results) {
    let message = `\n**2ms version: ${results['version']}**\n`;  

    // Cabeçalho da tabela
    message += "<table border='1' cellpadding='5' cellspacing='0'>\n";
    message += "<tr><th>Repo</th><th>Total Items Scanned</th></tr>\n";

    // Adiciona as linhas da tabela para cada repositório
    for (const [repo, data] of Object.entries(results)) {
        message += `<tr>
                        <td>${repo}</td>
                        <td>${data['total-items-scanned']}</td>
                    </tr>\n`;
    }

    message += "</table>\n\n";
    return message;
}

async function postJobSummary(results) {
    const message = createComment(results);
    await summary.addRaw(message).write();
}

module.exports = {
    postJobSummary
};
