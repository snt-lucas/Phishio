/**
 * Script responsável por gerenciar a ação de desinstalação na tela de manutenção.
 */
document.addEventListener("DOMContentLoaded", () => {
  const btnUninstall = document.getElementById("btn-uninstall");

  if (btnUninstall) {
    btnUninstall.addEventListener("click", () => {
      chrome.management.uninstallSelf({ showConfirmDialog: true }, () => {
        if (chrome.runtime.lastError) {
          console.log("O usuário cancelou a desinstalação.");
        }
      });
    });
  }
});
