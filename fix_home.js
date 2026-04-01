const fs = require('fs');
const files = fs.readdirSync('.').filter(f => f.endsWith('.html'));
files.forEach(file => {
    let content = fs.readFileSync(file, 'utf8');
    if (file !== 'index.html' && file !== 'home2.html') {
        // Desktop nav toggles for Home
        content = content.replace(/class="nav-link active flex items-center font-bold"([^>]*>\s*Home\s*<)/gi, 'class="nav-link flex items-center font-bold"$1');
        
        // Mobile drawer toggles for Home (might be text-accent-light or text-accent font-bold)
        content = content.replace(/class="block text-accent-light font-bold text-lg(.*?)id="mobile-homes-toggle"/gi, 'class="block text-primary-text font-bold text-lg$1id="mobile-homes-toggle"');
        content = content.replace(/class="block text-accent font-bold text-lg(.*?)id="mobile-homes-toggle"/gi, 'class="block text-primary-text font-bold text-lg$1id="mobile-homes-toggle"');
    }
    fs.writeFileSync(file, content);
});
console.log('done fixing home active links');
