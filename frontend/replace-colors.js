const fs = require('fs');
const path = require('path');

function walk(dir, callback) {
  fs.readdirSync(dir).forEach(f => {
    let dirPath = path.join(dir, f);
    let isDirectory = fs.statSync(dirPath).isDirectory();
    isDirectory ? walk(dirPath, callback) : callback(path.join(dir, f));
  });
}

walk('./src', function(filePath) {
  if (filePath.endsWith('.tsx') || filePath.endsWith('.ts')) {
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Replace surface text colors with text-muted
    content = content.replace(/text-surface-[3456]00/g, 'text-muted');
    
    // Replace white text with foreground (except in gradients or buttons if we can guess)
    // We'll replace all text-white and fix specific ones manually if needed, 
    // or we can use regex to avoid replacing if we see 'from-' or 'to-' or 'bg-brand' nearby in the same line
    let lines = content.split('\n');
    lines = lines.map(line => {
      if (line.includes('from-') || line.includes('bg-brand') || line.includes('to-purple') || line.includes('bg-red') || line.includes('text-white text-[10px]')) {
        // likely a gradient or colored badge, leave text-white alone
        return line;
      }
      return line.replace(/text-white/g, 'text-foreground')
                 .replace(/bg-surface-950(\/\d+)?/g, 'bg-background$1')
                 .replace(/bg-surface-900/g, 'bg-card')
                 .replace(/bg-white\/\[0\.03\]/g, 'bg-foreground/5')
                 .replace(/bg-white\/5/g, 'bg-foreground/5')
                 .replace(/border-white\/\[0\.0[0-9]\]/g, 'border-border')
                 .replace(/border-white\/10/g, 'border-border')
                 .replace(/hover:bg-white\/\[0\.03\]/g, 'hover:bg-foreground/5')
                 .replace(/bg-white\/10/g, 'bg-foreground/10');
    });
    
    fs.writeFileSync(filePath, lines.join('\n'));
  }
});
console.log('Done!');
