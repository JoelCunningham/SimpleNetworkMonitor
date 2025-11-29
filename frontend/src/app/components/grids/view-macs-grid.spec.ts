import { ViewMacsGrid } from '#components/grids';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('ViewMacsGrid', () => {
  let component: ViewMacsGrid;
  let fixture: ComponentFixture<ViewMacsGrid>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewMacsGrid],
    }).compileComponents();

    fixture = TestBed.createComponent(ViewMacsGrid);
    component = fixture.componentInstance;

    // Set required input
    component.device = {
      id: 1,
      model: 'Test Model',
      category: { id: 1, name: 'Test Category' },
      location: { id: 1, name: 'Test Location' },
      owner: null,
      name: 'Test Device',
      primary_mac: {
        id: 1,
        address: '00:11:22:33:44:55',
        last_ip: '192.168.1.100',
        last_seen: '2024-01-01T00:00:00Z',
        hostname: 'test-host',
        device: null,
        discoveries: [],
        ports: [],
      },
      macs: [],
    };

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
