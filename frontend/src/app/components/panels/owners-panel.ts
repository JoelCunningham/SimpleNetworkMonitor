import { OwnerAddCard } from '#components/cards/owner-add-card';
import { OwnerCard } from '#components/cards/owner-card';
import { OwnerModal } from '#components/modals/owner-modal';
import { BasePanel } from '#components/panels/base-panel';
import { Owner } from '#interfaces';
import { OwnerService } from '#services';
import { ChangeDetectorRef, Component } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-owners-panel',
  imports: [BasePanel, OwnerCard, OwnerAddCard, OwnerModal],
  templateUrl: './owners-panel.html',
  styleUrl: './owners-panel.scss',
})
export class OwnersPanel {
  protected owners: Owner[] = [];
  protected currentOwner: Owner | null = null;

  protected showOwnerModal = false;

  constructor(
    private ownerService: OwnerService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.ownerService.currentOwners().subscribe((data) => {
      this.owners = data.sort((a, b) => {
        const deviceDiff = (b.devices.length || 0) - (a.devices.length || 0);
        if (deviceDiff !== 0) return deviceDiff;
        return (a.name || '').localeCompare(b.name || '');
      });
      this.cdr.detectChanges();
    });
  }

  openViewModal(owner: Owner) {
    this.currentOwner = owner;
    this.showOwnerModal = true;
  }

  openAddModal() {
    this.currentOwner = { id: 0, name: '', devices: [] };
    this.showOwnerModal = true;
  }

  handleModalClose() {
    this.showOwnerModal = false;
  }
}
