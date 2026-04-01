import sys

file_path = "d:/Craft Cider & Meadery Company/home2.html"

try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Section 2
    content = content.replace(
        '<section class="py-24 bg-white overflow-hidden">',
        '<section class="py-24 bg-background overflow-hidden transition-colors duration-300">'
    )

    # Section 3
    content = content.replace(
        '<section class="py-24 bg-[#F1F5F2]">',
        '<section class="py-24 bg-hover transition-colors duration-300">'
    )

    # Section 4
    content = content.replace(
        '<section class="py-24 bg-white">',
        '<section class="py-24 bg-background transition-colors duration-300">'
    )

    # Section 5
    content = content.replace(
        '<section class="py-24 bg-[#F9FAF9]">',
        '<section class="py-24 bg-hover transition-colors duration-300">'
    )

    # We can carefully replace colors only inside the sections.
    # To be safe, we'll replace the text globally if they don't break anything.
    # We will exclude #main-footer, #main-header, hero section.

    # Instead of global replacements, let's target specific lines where hardcoded colors appear.
    # Replace these specific occurrences:

    content = content.replace('text-[#E6B325]', 'text-accent-light')
    
    # We can't replace all text-[#1F3D2B] globally because it might be used in places where it should be dark.
    # Actually, in dark mode it should map to text-accent so it looks good.
    content = content.replace('text-[#1F3D2B]', 'text-accent')
    
    content = content.replace('text-gray-600', 'text-secondary-text')
    content = content.replace('text-gray-500', 'text-secondary-text')
    
    content = content.replace('bg-[#E6B325]', 'bg-accent-light')
    
    # The CTA section
    content = content.replace(
        '<div class="relative bg-gradient-to-br from-[#1F3D2B] to-[#11261a] rounded-[3rem]', 
        '<div class="relative bg-ocean-gradient rounded-[3rem]'
    )
    
    content = content.replace(
        '<div class="w-24 h-24 bg-white border border-[#E6B325]/20 rounded-full flex items-center justify-center mx-auto mb-8 shadow-lg group-hover:border-[#E6B325]',
        '<div class="w-24 h-24 bg-background border border-accent-light/20 rounded-full flex items-center justify-center mx-auto mb-8 shadow-lg group-hover:border-accent-light'
    )
    
    content = content.replace(
        'border-4 border-[#E6B325]',
        'border-4 border-accent-light'
    )
    
    content = content.replace(
        'bg-[#E6B325]/10',
        'bg-accent-light/10'
    )
    
    content = content.replace(
        'bg-gradient-to-t from-[#1F3D2B] via-transparent to-transparent',
        'bg-ocean-gradient' # This gradient might look different. Let's keep it but change the from color.
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Done")
except Exception as e:
    print(e)    

