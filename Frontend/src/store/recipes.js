import { reactive } from 'vue'

import Hungarian_chicken from '@/assets/Hungarian_chicken.png'
import salmon_brocolli from '@/assets/salmon_brocolli.png'
import wraps from '@/assets/wraps.png'
import lemon_chicken from '@/assets/lemon_chicken.png'
import Tofu_sandwich from '@/assets/Tofu_sandwich.png'
import egg_fried from '@/assets/egg_fried.png'
import Ratatouille from '@/assets/Ratatouille.png'
import chickpeas_carrot_rice_bowl from '@/assets/chickpeas_carrot_rice_bowl.png'
import malaysian_inspired_chicken_rice from '@/assets/malaysian_inspired_chicken_rice.png'
import img1 from '@/assets/img1.gif'
import img2 from '@/assets/img2.jpg'
import img3 from '@/assets/img3.jpg'
import img4 from '@/assets/img4.jpg'
import img5 from '@/assets/img5.gif'
import img6 from '@/assets/img6.jpg'
import img7 from '@/assets/img7.gif'


export const recipes = reactive([
  { name: 'Hungarian Chicken Recipe', image: Hungarian_chicken, liked: false },
  { name: 'One-Skillet Salmon & Broccoli', image: salmon_brocolli, liked: false },
  { name: 'High Protein Wraps', image: wraps, liked: false },
  { name: 'Lemon Chicken Rice Bowl', image: lemon_chicken, liked: false },
  { name: 'Tofu Sandwiches', image: Tofu_sandwich, liked: false },
  { name: 'Fried Potato Egg Salad', image: egg_fried, liked: false },
  { name: '4-step Homemade Ratatouille', image: Ratatouille, liked: false },
  { name: 'Chickpeas Carrot Rice Bowl', image: chickpeas_carrot_rice_bowl, liked: false },
  { name: 'Malaysian Inspired Chicken Rice', image: malaysian_inspired_chicken_rice, liked: false }
])

export const images = [img1, img2, img3, img4, img5, img6, img7];

