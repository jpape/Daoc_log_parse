export class DefenseResults {
    constructor(
        public Hits: number,
        public Blocks: number,
        public TotalDamage: number,
        public SpellDamage: number,
        public Crits: number,
        public MeleeDamage: number,
        public Sources: string[],
        public Misses: number,
        public Evades: number,
        public Parries: number,
        public Resists: number,
        public TotalAttacks: number,
        public Absorbed: number,
        public SpellsLanded: number,
        public CritDamage: number,
        public TotalMeleeAttacks: number,
        public TotalSpellAttacks: number
    ) {}
}