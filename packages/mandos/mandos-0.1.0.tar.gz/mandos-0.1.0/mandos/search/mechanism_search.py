import logging
from dataclasses import dataclass
from typing import Sequence

from pocketutils.core.dot_dict import NestedDotDict

from mandos.model import ChemblCompound
from mandos.model.targets import Target
from mandos.search.protein_search import ProteinHit, ProteinSearch

logger = logging.getLogger("mandos")


@dataclass(frozen=True, order=True, repr=True, unsafe_hash=True)
class MechanismHit(ProteinHit):
    """
    A mechanism entry for a compound.
    """

    action_type: str
    direct_interaction: bool
    description: str
    exact_target_id: str

    @property
    def predicate(self) -> str:
        return self.action_type.lower()


class MechanismSearch(ProteinSearch[MechanismHit]):
    """
    Search for ``mechanisms``.
    """

    def query(self, parent_form: ChemblCompound) -> Sequence[NestedDotDict]:
        return list(self.api.mechanism.filter(parent_molecule_chembl_id=parent_form.chid))

    def should_include(self, lookup: str, compound: ChemblCompound, data: NestedDotDict) -> bool:
        # no conceivable problems not related directly to the target (which are handled in the superclass)
        return True

    def to_hit(
        self, lookup: str, compound: ChemblCompound, data: NestedDotDict, target: Target
    ) -> Sequence[MechanismHit]:
        # these must match the constructor of the Hit,
        # EXCEPT for object_id and object_name, which come from traversal
        x = NestedDotDict(
            dict(
                record_id=data["mec_id"],
                compound_id=compound.chid,
                inchikey=compound.inchikey,
                compound_name=compound.name,
                compound_lookup=lookup,
                action_type=data["action_type"],
                direct_interaction=data["direct_interaction"],
                description=data["mechanism_of_action"],
                exact_target_id=data["target_chembl_id"],
            )
        )
        return [MechanismHit(**x, object_id=target.chembl, object_name=target.name)]


__all__ = ["MechanismHit", "MechanismSearch"]
