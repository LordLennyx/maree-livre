// Texte de l'extrait — source unique pour la liseuse, le PDF intérieur et l'EPUB.
const LIVRE = {
  titre: "Ce que la marée rapporte",
  auteur: "Danièle Nkotto",
  editeur: "Éditions du Littoral",
  annee: 2026,
  dedicace: "À ma grand-mère, qui comptait les vagues pour s'endormir.",
  chapitres: [
    { titre: "La bouteille verte", paras: [
      "La mer avait rendu la bouteille un mardi, à l'heure où les pirogues rentrent et où les enfants de Londji courent sur le sable mouillé pour voir ce que les filets ont pris. Awa ne courait plus depuis longtemps. Elle avait onze ans quand elle était partie pour Douala, trente-quatre quand elle était revenue, et entre les deux il y avait eu une ville entière, un métier, un mariage qui n'avait pas tenu, et ce silence qu'on rapporte des grandes villes comme on rapporte du sable dans ses chaussures.",
      "La bouteille était verte, épaisse, de celles qu'on ne fabrique plus. Un bouchon de liège noirci la fermait, recouvert d'une cire qui avait dû être rouge. Elle roulait au bord de l'eau, à chaque vague un peu plus loin, un peu plus près, comme si elle hésitait.",
      "Awa la ramassa sans réfléchir. Elle était froide, lisse, plus lourde qu'elle ne l'aurait cru. À travers le verre, on devinait un papier roulé serré, attaché par un fil de raphia.",
      "« Tu vas l'ouvrir ? » demanda une voix derrière elle.",
      "C'était le fils de la voisine, Junior, huit ans, qui suivait tout ce qui bougeait sur la plage avec la gravité d'un inspecteur. Il avait les genoux couverts de sable et une crevette morte dans la main droite, qu'il semblait avoir oubliée.",
      "« Pas ici, répondit Awa. Les choses qui viennent de la mer, on les ouvre à la maison. »",
      "Elle ne savait pas d'où lui venait cette phrase. Puis elle s'en souvint : c'était celle de sa grand-mère, Mama Ngo, qui ramassait autrefois tout ce que l'océan déposait — des flotteurs, des sandales orphelines, une fois un réveil japonais qui marchait encore — et qui refusait d'en examiner un seul avant d'avoir posé la marmite sur le feu.",
      "Junior hocha la tête, comme si la règle était connue de tous. Il la raccompagna jusqu'à la maison aux volets bleus, celle que tout le village appelait encore la maison de Mama Ngo, alors que Mama Ngo était morte depuis six semaines."
    ]},
    { titre: "La maison aux volets bleus", paras: [
      "La maison sentait le bois humide, le pétrole de lampe et quelque chose de plus ancien, de plus doux, qu'Awa n'arrivait pas à nommer. Peut-être simplement l'odeur de quelqu'un qui a vécu longtemps au même endroit et qui a fini par se mêler aux murs.",
      "Depuis son retour, Awa dormait dans la petite chambre du fond, celle de son enfance. Elle n'avait pas encore osé ouvrir l'armoire de sa grand-mère. Les robes y étaient pendues dans l'ordre exact où Mama Ngo les portait : le pagne du dimanche, le pagne du marché, le pagne des deuils, qu'elle avait mis plus souvent qu'aucun autre.",
      "Elle posa la bouteille sur la table de la cuisine, à côté du seau d'eau et de la boîte de sel. Puis, parce que la règle le voulait, elle alluma le feu, fit chauffer de l'eau et prépara un thé à la citronnelle avec les feuilles qui poussaient derrière la maison, là où Mama Ngo les avait plantées quarante ans plus tôt.",
      "La cire céda sous la lame du couteau. Le bouchon résista, puis sortit d'un coup, avec un petit bruit sec qui fit sursauter Awa. Une odeur s'échappa du goulot, si légère qu'elle crut l'avoir rêvée : celle du savon de karité que sa grand-mère achetait par pains entiers au marché de Kribi.",
      "Le papier était plié en quatre, puis roulé. Il avait jauni sans se déchirer. L'écriture était penchée, appliquée, celle des gens qui ont appris à écrire à l'école des missionnaires et qui n'ont jamais tout à fait perdu la peur de la faute.",
      "La lettre commençait par ces mots : « À la personne qui trouvera ceci, je vous demande pardon de vous déranger. »",
      "Awa relut la phrase trois fois. Elle reconnaissait cette écriture. Elle l'avait vue sur des cartes d'anniversaire, sur des listes de courses, sur le cahier où Mama Ngo notait le prix du poisson depuis 1971.",
      "La bouteille avait été jetée à la mer par sa grand-mère."
    ]},
    { titre: "Pardon de vous déranger", paras: [
      "« À la personne qui trouvera ceci, je vous demande pardon de vous déranger. Je m'appelle Régine Ngo Bilong et j'habite Londji, au sud de Kribi, dans la maison aux volets bleus. Si vous lisez cette lettre, c'est que la mer a décidé de vous la confier, et je fais confiance à la mer, même si elle m'a pris un mari et deux frères. »",
      "Awa dut s'asseoir. Dehors, le soleil descendait vers l'eau et tout devenait orange, les murs, les mains, la bouteille vide sur la table.",
      "« J'ai une petite-fille qui s'appelle Awa. Elle a onze ans aujourd'hui et elle part demain pour Douala, chez sa tante, pour aller au collège. C'est une bonne chose. Ici il n'y a que la mer, et la mer ne donne pas de diplômes. Mais je sais comment sont les villes. On y entre enfant et on en sort fatigué. On y oublie le bruit des vagues, et après on ne dort plus. »",
      "« Alors je fais une chose idiote, et je vous demande de ne pas vous moquer. J'écris les choses que je voudrais lui dire quand elle sera grande, et je les confie à l'océan, parce que je n'ai pas d'autre facteur assez patient. Il y aura d'autres bouteilles. Une chaque année, le jour de son anniversaire, tant que mes jambes me porteront jusqu'au bout de la jetée. »",
      "Awa porta la main à sa bouche. Elle se souvenait de ce jour-là, du car pour Douala, de sa grand-mère restée debout sur le bord de la route, toute droite, sans agiter la main, parce qu'agiter la main, disait-elle, c'est pour les gens qui ne sont pas sûrs de se revoir.",
      "« Si un jour cette lettre arrive jusqu'à elle, par un miracle que je ne verrai sans doute pas, voici ce que je veux qu'elle sache. Awa, tu as le droit de revenir. Même tard. Même sans rien avoir réussi de ce que les gens attendaient. La maison t'attendra. Les volets sont bleus pour que tu les reconnaisses depuis la mer. »",
      "La lettre était signée d'un simple R, suivi d'une date : le 14 septembre 1999.",
      "Awa resta longtemps sans bouger. Puis elle se leva, sortit sur le pas de la porte et regarda la mer, qui continuait de monter avec la même indifférence tranquille. Quelque part, peut-être, d'autres bouteilles dérivaient encore."
    ]},
    { titre: "Le cahier du prix du poisson", paras: [
      "Le lendemain, Awa ouvrit l'armoire.",
      "Elle le fit d'un geste, sans se laisser le temps d'hésiter, comme on entre dans l'eau froide. Les robes étaient là, et l'odeur aussi, et pendant un instant elle crut qu'elle allait pleurer. Mais elle ne pleura pas. Elle chercha.",
      "Le cahier était sur l'étagère du haut, sous une pile de draps repassés. Un cahier d'écolier à couverture bleue, gonflé par l'humidité, que Mama Ngo appelait le cahier du prix du poisson. Awa l'avait toujours vu sur la table de la cuisine, ouvert à la page du jour, avec ses colonnes bien alignées : bars, capitaines, crevettes, carpes, et le prix en face, au franc près.",
      "Elle le feuilleta. 1971, 1972, 1973. Les prix montaient lentement, avec les années, comme une marée de chiffres. Puis, en 1999, au milieu des colonnes, une ligne différente : « 14 septembre. Bouteille n° 1. Jetée à la pointe, marée descendante. »",
      "Awa tourna les pages plus vite. Chaque année, à la même date, la même ligne. « Bouteille n° 2. » « Bouteille n° 3. » Parfois un mot de plus : « vent fort », « Junior m'a aidée », « j'ai mal aux genoux mais j'y suis allée ». La dernière ligne datait de l'année précédente. « Bouteille n° 24. Je ne sais pas si j'irai jusqu'à la vingt-cinquième. Ce n'est pas grave. La mer a l'habitude d'attendre. »",
      "Vingt-quatre bouteilles. Vingt-quatre lettres. Une seule était revenue.",
      "Awa referma le cahier et le serra contre elle. Dehors, Junior l'attendait déjà sur la plage, sa crevette de la veille remplacée par un crabe vivant qu'il tenait avec précaution entre deux doigts.",
      "« Alors, demanda-t-il, c'était quoi, dans la bouteille ? »",
      "Awa s'assit à côté de lui, face à l'eau. Le soleil montait derrière eux et la mer était d'un vert presque gris, calme, attentive.",
      "« Une lettre, dit-elle. Et une liste de choses à chercher. »",
      "Junior la regarda avec sérieux. « Tu vas chercher les autres ? »",
      "Elle ne répondit pas tout de suite. Elle pensait aux courants, aux kilomètres, aux plages du Gabon, de Sao Tomé, peut-être plus loin encore, où des bouteilles vertes avaient pu s'échouer, être ramassées, jetées, oubliées. C'était absurde. C'était impossible.",
      "« Oui, dit-elle enfin. Je vais chercher les autres. »",
      "Et pour la première fois depuis des années, cette nuit-là, elle dormit en écoutant les vagues."
    ]}
  ]
};
if (typeof module !== "undefined") module.exports = LIVRE;
