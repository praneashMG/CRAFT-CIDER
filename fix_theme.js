const fs = require('fs');
const file = 'index.html';
let content = fs.readFileSync(file, 'utf8');

// Update CSS utilities
content = content.replace(
  /\.border-border \{ border-color: var\(--color-border\); \}/,
  '.border-border { border-color: var(--color-border); }\n        .bg-accent { background-color: var(--color-accent); }\n        .bg-accent-light { background-color: var(--color-accent-light); }'
);

// 2. Our Story
content = content.replace(/<section class="py-24 bg-white overflow-hidden">/, '<section class="py-24 bg-background overflow-hidden">');
content = content.replace(/class="text-\[#E6B325\] /g, 'class="text-accent-light ');
content = content.replace(/text-\[#1F3D2B\]/g, 'text-accent');
content = content.replace(/text-gray-600/g, 'text-secondary-text');
content = content.replace(/bg-\[#E6B325\]/g, 'bg-accent-light');

// 3. Our Philosophy / Values
content = content.replace(/bg-\[#F1F5F2\]/g, 'bg-hover');
content = content.replace(/class="bg-white p-10/g, 'class="bg-background border border-border p-10');
content = content.replace(/text-gray-500/g, 'text-secondary-text');
content = content.replace(/group-hover:bg-\[#1F3D2B\]/g, 'group-hover:bg-accent');
content = content.replace(/bg-\[#1F3D2B\]/g, 'bg-accent');
content = content.replace(/text-\[#E6B325\]/g, 'text-accent-light');

// 4. Our Process 
content = content.replace(/<section class="py-24 bg-white">/, '<section class="py-24 bg-background">');

// 5. Team 
content = content.replace(/class="group bg-white /g, 'class="group bg-background border border-border ');

fs.writeFileSync(file, content);
console.log("Replaced successfully!");
